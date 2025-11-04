# 🛒 Serverless Order Processing System

A fully serverless e-commerce order processing pipeline built using **AWS S3**, **API Gateway**, **Lambda**, **SQS**, and **DynamoDB**.  
This system accepts user orders from a static website, queues them for processing, and stores the finalized order records in DynamoDB — all without managing any servers.

---

## 🚀 Architecture Overview

![Architecture Diagram](./screenshots/architecture-diagram.png)

### Flow:

1. **User Interaction** – A user submits an order through a static website hosted on **Amazon S3**.  
2. **API Gateway** – The static site sends the order request to an **API Gateway REST API**.  
3. **Lambda Function (API Handler)** – The API Gateway triggers a **Lambda function**, which validates and pushes the order data into an **SQS Queue**.  
4. **SQS Queue** – Acts as a buffer to handle large traffic and decouple the frontend from backend processing.  
5. **Lambda Function (Processor)** – Another **Lambda** reads messages from SQS, processes them, and writes the final record to a **DynamoDB Table**.  
6. **DynamoDB Table** – Stores order information reliably and scales automatically.

---

## 🧩 AWS Services Used

| Service | Purpose |
|----------|----------|
| **Amazon S3** | Hosts the static frontend website |
| **Amazon API Gateway** | Exposes REST endpoints to the frontend |
| **AWS Lambda** | Handles API requests and background processing |
| **Amazon SQS** | Message queue for decoupling frontend and backend |
| **Amazon DynamoDB** | Stores order details persistently |

---

## 📸 AWS Console Screenshots

### 1. S3 Bucket Configuration
![S3 Bucket Setup](./screenshots/01-s3-bucket-config.png)
*Static website hosting enabled for the frontend*

### 2. API Gateway Configuration
![API Gateway](./screenshots/02-api-gateway-setup.png)
*REST API endpoints configured for order submission*

### 3. Lambda Function - Submit Order
![Submit Order Lambda](./screenshots/03-lambda-submit-order.png)
*Lambda function that receives orders from API Gateway*

### 4. Lambda Function - Process Order
![Process Order Lambda](./screenshots/04-lambda-process-order.png)
*Lambda function that processes orders from SQS*

### 5. SQS Queue Configuration
![SQS Queue](./screenshots/05-sqs-queue-config.png)
*Message queue for asynchronous order processing*

### 6. DynamoDB Table Structure
![DynamoDB Table](./screenshots/06-dynamodb-table.png)
*Orders table with partition key and attributes*

### 7. Working Application Demo
![Application Demo](./screenshots/07-application-demo.png)
*Frontend interface for order submission*

### 8. DynamoDB Records (Optional)
![DynamoDB Records](./screenshots/08-dynamodb-records.png)
*Sample order records stored in the database*

---

## ⚙️ Technologies

- **Frontend:** HTML, CSS, JavaScript (hosted on S3)
- **Backend:** AWS Lambda (Node.js or Python)
- **Database:** DynamoDB
- **Integration:** API Gateway + SQS

---

## 🧠 Key Features

- ✅ 100% Serverless and Auto-scalable  
- 📦 Asynchronous order processing using **SQS**  
- 🧱 Reliable storage with **DynamoDB**  
- ⚡ Fast, secure, and cost-efficient  
- 🔍 Event-driven architecture  

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/serverless-order-system.git
   cd serverless-order-system
   ```

2. **Create AWS Resources**
   - Create an **S3 bucket** and enable static website hosting.
   - Deploy an **API Gateway REST API**.
   - Create two Lambda functions:
     - `submitOrderLambda` – Sends order details to SQS.
     - `processOrderLambda` – Reads from SQS and writes to DynamoDB.
   - Create an **SQS Queue**.
   - Create a **DynamoDB table** named `Orders`.

3. **Deploy Lambda Functions**
   - Upload your Lambda code via AWS Console or using AWS CLI:
     ```bash
     aws lambda update-function-code --function-name submitOrderLambda --zip-file fileb://submitOrder.zip
     ```

4. **Update API Gateway Integration**
   - Link the POST endpoint to the `submitOrderLambda`.

5. **Test the Flow**
   - Open your static site URL.
   - Submit an order.
   - Check DynamoDB for the new record.

---

## 📁 Folder Structure

```
serverless-order-system/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── lambdas/
│   ├── submitOrderLambda.js
│   └── processOrderLambda.js
│
├── screenshots/
│   ├── architecture-diagram.png
│   ├── 01-s3-bucket-config.png
│   ├── 02-api-gateway-setup.png
│   ├── 03-lambda-submit-order.png
│   ├── 04-lambda-process-order.png
│   ├── 05-sqs-queue-config.png
│   ├── 06-dynamodb-table.png
│   ├── 07-application-demo.png
│   └── 08-dynamodb-records.png
│
└── README.md
```

---

## 🧾 Example DynamoDB Record

```json
{
  "orderId": "12345",
  "customerName": "John Doe",
  "product": "Laptop",
  "quantity": 1,
  "status": "Processed",
  "timestamp": "2025-11-03T12:47:44Z"
}
```

---

## 💡 Future Enhancements

- Add **SNS notifications** for order confirmation
- Integrate **Step Functions** for workflow orchestration
- Add authentication using **AWS Cognito**
- Implement **CloudWatch** monitoring and alerts
- Add **API Gateway authorization** for enhanced security

---

## 👨‍💻 Author

**Abhishek Rangnath Kanade**  
MERN Stack & Serverless Developer  
📍 Pune, India  
🔗 [LinkedIn](https://linkedin.com/in/abhishekk) | [Portfolio](https://abhishekk.dev)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.