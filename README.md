![Main Banner](gh-assets/readme-banner.png)

<h2>Game Oracle</h2>

<h5>A truly Customisable and Personalised Game Database experience.</h5>

An OpenAI powered game database that allows you to look up games and find out whatever you want about it whilst OpenAI helps to customise each page around the game you are viewing.



<p>
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#prompt-help">Prompt Help</a> •
  <a href="#example-output">Example Output</a> •
  <a href="#credits">Credits</a> 
</p>




## Key Features

![Key Features Banner](gh-assets/key-features-banner.png)

* **Find Any Game by Title**
  
  - Search for a game title and ask anything about it
  
* **Personalised Descriptions**
  
  - Ask the Bot what a game is and expect a personalised description that matches the games story and feel
  
* **Find Game Stores**

  - Find where you can buy games you want to purchase with direct links

* **Find Game Communities**

  - Find out whether or not a game has a Reddit community to get involved and ask some questions before purchasing

* **Find Out What People Think**

  - Ask the Bot what players think of a specific game for real community ratings and opinions

* **Custom Background**

  - Watch as the Webpage changes to the video game you are researching

* **Conversational Experience**

  - Have a conversation about the game and see what you find out!

    

## How To Use

![How To Use Banner](gh-assets/how-to-use-banner.png)

Before trying to run this application, please ensure you install all of the correct libraries to a virtual environment.

> **Note**
> Please refer to the [**requirements.txt**] in the repository to install all of the correct and up-to-date libraries.



1) **Set up your Azure Key & Endpoint**:

   Firstly, ensure you have an OpenAI Azure account with a key and endpoint.

   After this, modify *main.py* to access these values and set them to the `api_key` and `azure_endpoint` variables.

   > **Note**
   >
   > By base, the Key & Endpoint are being read by the OS which can be defined within your command prompt. Keep these values secure and safe.
2. **Set up your RAWG API Account:**

   Set up an [API Account](https://rawg.io/) on RAWG io and then login.

   When you are logged in, go to the [developer portal](https://rawg.io/apidocs) to access your personal *API key*.

   Ensure that these are being read correctly by the bot.py script.

   ![Dashboard](gh-assets/Dashboard.png)

   > **Note**
   >
   > Keep your RAWG Key private and secure

3. **Read your RAWG Key:**

   Within your project directory, create a new folder called `keys` and create a new JSON file named `rawg_keys`.
   
   Copy paste the text below and replace `YOUR_KEY_HERE` with **your RAWG key**.
   
   ```json
   {
       "client_key": "YOUR_KEY_HERE",
       "base_url": "https://api.rawg.io/api/games"
   }
   ```
   
4. **Run Flask:**

   Run the Flask app within your command prompt by typing `flask run`.

   > **Note:**
   >
   > Ensure you have your virtual environment active when doing so

5. **Explore Some Games:**

   Feel free to now look up some games and get the information you want!



## Prompt Help

![Help Page Banner](gh-assets/help-banner.png)

If you are struggling with getting the correct data back, this may be down to your **prompt** wording.

To ensure you are using proper prompts, please ensure you refer to the **Help Page** located on the top right hand side of the webpage.




## Example Output

**Soon**



## Credits

**Soon**

Huge thanks to:

- [Azure](https://azure.microsoft.com/en-gb/pricing/purchase-options/azure-account/search?icid=free-search&ef_id=_k_CjwKCAiA3ZC6BhBaEiwAeqfvyjldSpYmnBiBxu3p14RMM4OA8yQiS7emMeiyQpGL3UymUj-DJfJwYxoCEGsQAvD_BwE_k_&OCID=AIDcmm3bvqzxp1_SEM__k_CjwKCAiA3ZC6BhBaEiwAeqfvyjldSpYmnBiBxu3p14RMM4OA8yQiS7emMeiyQpGL3UymUj-DJfJwYxoCEGsQAvD_BwE_k_&gad_source=1&gclid=CjwKCAiA3ZC6BhBaEiwAeqfvyjldSpYmnBiBxu3p14RMM4OA8yQiS7emMeiyQpGL3UymUj-DJfJwYxoCEGsQAvD_BwE)
- [RAWG.io](https://rawg.io/)