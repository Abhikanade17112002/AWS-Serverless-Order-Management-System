import json
import logging
import traceback
from boto3.dynamodb.types import TypeDeserializer

# --- Setup logger ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- DynamoDB deserializer ---
deserializer = TypeDeserializer()


def _unmarshall(dynamodb_map):
    """Convert DynamoDB stream map into standard JSON."""
    if not dynamodb_map:
        return None
    return {k: deserializer.deserialize(v) for k, v in dynamodb_map.items()}


def _normalize_records(event):
    """Handle DynamoDB Stream, EventBridge Pipe, or custom event (object/list)."""
    # Handle if event is a list (your current case)
    if isinstance(event, list):
        records = []
        for item in event:
            if 'orders' in item and isinstance(item['orders'], list):
                records.extend([{'custom': True, 'order': order} for order in item['orders']])
        return records

    # Normal object cases
    if 'Records' in event:
        return event['Records']
    if 'detail' in event and isinstance(event['detail'], dict):
        if 'records' in event['detail']:
            return event['detail']['records']
        if 'dynamodb' in event['detail']:
            return [{'dynamodb': event['detail']['dynamodb'], 'eventName': event['detail'].get('eventName')}]
    if 'orders' in event and isinstance(event['orders'], list):
        return [{'custom': True, 'order': order} for order in event['orders']]

    return []


def handle_order(order):
    """Simulate business logic for valid orders."""
    logger.info(f"🛠 Handling order: {order.get('orderId')} | Amount: {order.get('amount')} | Status: {order.get('status')}")
    # Example: send to another service, DB, SNS, etc.
    return True


def lambda_handler(event, context):
    """Main Lambda handler."""
    logger.info("🚀 Lambda Execution Started")
    logger.info(f"📥 Incoming event: {json.dumps(event, indent=2)}")

    records = _normalize_records(event)
    failed = []
    valid_orders = []

    logger.info(f"🔎 Found {len(records)} records to process")

    for rec in records:
        try:
            if rec.get('custom'):
                order = rec['order']
            else:
                ddb = rec.get('dynamodb', {})
                order = _unmarshall(ddb.get('NewImage')) or _unmarshall(ddb.get('OldImage'))

            if not order:
                logger.warning(f"⚠️ Empty order data found in record: {rec}")
                continue

            order_id = order.get("orderId")
            status = order.get("status")
            amount = float(order.get("amount", 0))
            email = order.get("customerEmail")

            logger.info(f"🧩 Processing order: ID={order_id}, Status={status}, Amount={amount}, Email={email}")

            if amount > 100:
                valid_orders.append(order)
                logger.info(f"✅ Order {order_id} passed filter (Amount={amount})")
                handle_order(order)
            else:
                logger.warning(f"🚫 Order {order_id} skipped (Amount={amount} ≤ 100)")

        except Exception as ex:
            error_details = traceback.format_exc()
            logger.error(f"❌ Error processing record: {ex}\n{error_details}")
            failed.append({"error": str(ex), "record": rec})

    logger.info("📊 Processing Summary:")
    logger.info(f"   ✅ Valid orders processed: {len(valid_orders)}")
    logger.info(f"   ❌ Failed records: {len(failed)}")
    logger.info("🏁 Lambda Execution Completed")

    if failed:
        raise Exception("Some records failed: " + json.dumps(failed))

    return {
        "status": "ok",
        "processed": len(valid_orders),
        "validOrders": valid_orders
    }
