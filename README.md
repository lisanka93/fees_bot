# Persuasive Chatbot on the Topic of UK University Fees (Flask Facebook Chatbot)


### 1. Set up a Facebook Application
#### 1.1. Create app
Go to: https://developers.facebook.com/apps
Create a new application with a random name. Next, when prompted on the next page for the type of product you are building, click the “Set Up” button on the Messenger option.

![Image of step_1](https://i.imgur.com/fhV34om.png)

#### 1.2. Generate Access token
After you were redirected on the Settings page, you need to select or create a specific Facebook Page (Public community or other) to assign to your bot.

![Image of Step_2](https://i.imgur.com/4dWhMMD.png)

![Image of Step_3](https://i.imgur.com/qns9PZ6.png)

Now, you need to Generate Token for your app and actually paste this FB token to your application in `app.py` find `ACCESS_TOKEN = 'GENERATED_TOKEN_FROM_FACEBOOK'` and change value with your generated token.

#### 1.3. Create Verify Token
Next, in the `VERIFY_TOKEN` value put any variable you want. To protect your bot, Facebook requires you to have a verify token. When a user messages your bot, Facebook will send your bot the message along with this verify token for your Flask app to check and verify the message is an authentic request sent by Facebook. Choose a string you want to use for your verify token and replace the placeholder in the app.py file with your code (ex. “TESTINGTOKEN” could be your verify token, but I’d recommend something harder for someone to guess) and place the same token (minus the quotation marks) in the Verify Token field.

### 2. Host Chatbot

I hosted mine on my university server on a virtual machine. But there are many other ways - e.g. Heroku


### 3. Set up Webhook
In Facebook Developer Center, in your Messenger settings, add a Callback URL to Webhooks section:
![Image of step_6](https://i.imgur.com/X9g2NdM.png)

Here, you will need to paste URL to your heroku app (we copied it in previous step), and into another field put the value (VERIFY_TOKEN = YOUR_CREATED_VALUE) you've created in step 1.3. 

If you've did all right, Facebook will test this callback and add this to the app. After that, for the subscription fields, be sure to check the messages, messaging_postbacks, message_deliveries, messaging_pre_checkouts boxes:
![Image of Step_7](https://i.imgur.com/KQ32ztw.png)

So, it was a final step. Go to your messages in Facebook, create a new message and send it to previously created community/group. 

![Image of final](https://i.imgur.com/eZ1fytL.png)

Enjoy & Thank you! :clap: :raised_hands:

Alternative deployment, using ngrok is [here](https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html)
