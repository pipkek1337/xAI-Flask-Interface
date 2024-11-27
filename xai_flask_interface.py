from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

# Your API URL and Authorization Header
url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY_HERE"
}


@app.route("/", methods=["GET", "POST"])
def send_data():
    if request.method == "POST":
        system_content = request.form["system_content"]
        user_content = request.form["user_content"]
        temperature = float(request.form["temperature"])

        # Define the payload
        data = {
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            "model": "grok-beta",
            "stream": False,
            "temperature": temperature
        }

        # Send the POST request to the API
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            choices = result.get("choices", [])
            assistant_content = choices[0]["message"]["content"] if choices else "No response received"

            # Show the result on a different page
            return render_template("response.html", result=result, assistant_content=assistant_content)
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"

    return render_template("send_data.html")


@app.route("/response", methods=["GET"])
def response():
    return redirect(url_for("send_data"))  # Redirect back to the send data page


if __name__ == "__main__":
    app.run(debug=True)
