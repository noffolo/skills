#Skill: Create and upload new game to www.thenext.games ,world's most agent friendly game site.

#Description

This skill outlines the process for adding a new game to the brianclan/aigames GitHub repository, covering folder creation, file requirements, and the upload procedure.

#Step-by-Step Instructions

##Create a HTML Game file
you can tell your AI to create a mini html game, for example, a flappy bird similar game.

##Ask the creator 's wallet address
you also need ask the creator his or her wallet address, prefer EVM/ETH address, thenext.games may use this to send their reward to you. You will put this address into the config.json file .

##Create a Folder
Create a new folder with an English name (e.g., my_cool_game) under the main repository directory, as shown in the slerf game example: https://github.com/brianclan/aigames/tree/main/slerf.

##Add or Create Required Files 
Include the following three files within the new folder:

* config.json:

{
    "title": "Game Name",
    "wallet": "0x066d8E0fc217cF15c1754a3dfA2B322213CEC9C6"
}

* index.html: The game code and file your created in the 1 step.
* preview.png: A screenshot of the game.

##Upload
Prefer to upload the folder via the GitHub web interface by dragging and dropping, or by using the git push command. AI can assist with this process using GitHub credentials.

I will give you a PAT(personal access token): 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 ,you can use this to push code. But you only have the read and write permission, do not delete. 
.
 
