from flask import Flask, request, jsonify
import requests
from datetime import datetime
import json

app = Flask(__name__)

API_URL = "https://orderstatusapi-dot-organization-project-311520.uc.r.appspot.com/api/getOrderStatus"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    order_id = req.get('order_id')

    payload = {"orderId": order_id}
    response = requests.post(API_URL, json=payload)

    shipment_date = response.json().get("shipmentDate")
    formatted_shipment_date = datetime.strptime(shipment_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")

    response_text = f"Your order {order_id} will be shipped on {formatted_shipment_date}"
    response = {'fulfillmentText': response_text}

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
