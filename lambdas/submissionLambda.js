// index.js - SubmissionLambda
const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { PutCommand, DynamoDBDocumentClient } = require("@aws-sdk/lib-dynamodb");
const { v4: uuidv4 } = require("uuid");

const REGION = process.env.AWS_REGION || "ap-south-1";
const TABLE = process.env.TABLE_NAME || "UserSubmissions";

const client = new DynamoDBClient({ region: REGION });
const ddb = DynamoDBDocumentClient.from(client);

exports.handler = async (event) => {
  try {
    const body = event.body ? JSON.parse(event.body) : {};
    const { name, email, message } = body;

    if (!name || !email || !message) {
      return {
        statusCode: 400,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        body: JSON.stringify({ error: "name, email and message are required." })
      };
    }

    const submissionId = uuidv4();
    const submissionDate = new Date().toISOString();
    const status = "NEW";

    const item = { submissionId, name, email, message, submissionDate, status };

    await ddb.send(new PutCommand({ TableName: TABLE, Item: item }));

    return {
      statusCode: 201,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ submissionId, message: "Submission saved." })
    };

  } catch (err) {
    console.error(err);
    return {
      statusCode: 500,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ error: "Internal server error" })
    };
  }
};
