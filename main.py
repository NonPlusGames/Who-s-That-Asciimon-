# ___________                                   .__      ___.                  
# \__    ___/___ _____    _____   ____________  |__| ____\_ |__   ______  _  __
#   |    |_/ __ \\__  \  /     \  \_  __ \__  \ |  |/    \| __ \ /  _ \ \/ \/ /
#   |    |\  ___/ / __ \|  Y Y  \  |  | \// __ \|  |   |  \ \_\ (  <_> )     / 
#   |____| \___  >____  /__|_|  /  |__|  (____  /__|___|  /___  /\____/ \/\_/  
#              \/     \/      \/              \/        \/    \/               
# coded by: Rafael Ivan Mota

from ascii_magic import AsciiArt
from termcolor import colored
import requests
import json
import random
import os
import sys

class NewGame:
  def __init__(self):
    self.player={}
    self.difficulty = 1
    self.hintNumber = 3
    self.score = 0
    self.pokemon = "default"
    self.tries = 3

def rules():
  print("""
RULES:
1) You have 3 guesses to correctly name the pokemon. The shorter number of guesses the more points.
2) You have access to a total of 3 hints for the whole game.
3) If you ever get all three guesses wrong.  The game will end and save your High Score.

INSTRUCTIONS:
When you encounter this symbol [::] type in your response and press [ENTER].
Type [manual] to read the rules and instructions again.
Type [pokemon] to display the current pokemon.
Type [hint] to use up one of your hints.
Type [score] to show your current score and number of available hints.
Type [restart] to start a new game.
  """)

def intro():
  print("""
Thankyou for playing [Who's That Asciimon!].
This game is a riff on 'Who's That Pokemon!', which appeared in-between episodes of the cartoon
adaptation of the widely popular video game series 'Pokemon'.  Much like the series, this game
will show you a silhouette of a random pokemon made out of ascii characters and you have to guess who it is.  
Please refer to the following rules while playing.  Have Fun!

RULES:
1) You have 3 guesses to correctly name the pokemon. The shorter number of guesses the more points.
2) You have access to a total of 3 hints for the whole game.
3) If you ever get all three guesses wrong.  The game will end and save your High Score.

INSTRUCTIONS:
When you encounter this symbol [::] type in your response and press [ENTER].
Type [guess] to make a guess at the pokemon
Type [manual] to read the rules and instructions again.
Type [pokemon] to display the current pokemon.
Type [hint] to use up one of your hints.
Type [score] to show your current score and number of available hints.
Type [restart] to start a new game.
  """)
# Prompt and set the difficulty for the player.  Checks that they make the correct input.
def setDiff():
  level = input("""
  Please select a difficulty:
  1: Easy
  2: Normal
  3: Hard
  :: """)
  try:
    level = int(level)
  except ValueError:
    print(colored("Please try again. Type 1, 2, or 3.", "red", attrs=["bold"]))
    return setDiff()
  if(level>3 or level<=0):
    print(colored("Please try again. Type 1, 2, or 3.", "red", attrs=["bold"]))
    return setDiff()
  return level

#Generate a pokemon based on the current instance of the game and return a dict [hints] with hints based
#off of that individual pokemon
def generatePokemon(ng):
  hints = [] #list of hints to be generated based of a specific pokemon
  name = ""
  type = ""
  ability= ""
  #generate a random pokemonID and save the api data associated with it to a file [data.json]
  random_poke_ID = random.randint(1,151)
  response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random_poke_ID}")
  data = response.json()
  with open("data.json", "w") as f:
    json.dump(data, f)
 
  #Grab the sprite from the api data and save it to a file named [pokemon.png]
  image_url = data["sprites"]["front_default"]
  image_response = requests.get(image_url)
  with open('pokemon.png', 'wb') as f:
    f.write(image_response.content)
  
  #iterate through the [type] data and store all of it's types
  for types in data["types"]:
    type=type+types["type"]["name"]+" "

  #iterate through the [ability] data and store all of it's abilities
  for abilities in data["abilities"]:
    ability=ability+abilities["ability"]["name"]+" "
    
  #iterate through the name and store and create a hint using the first and last letters
  name = data["name"]
  nameHint=""
  for i in range(0, len(name)):
    if i==0:
      nameHint += name[i]
    elif i==(len(name)-1):
      nameHint += name[i]
    else:
      nameHint += "_"

  #Save [name] [type] and [ability] to the [hints] dict
  hints.append("name: "+nameHint)
  hints.append("type: "+type)
  hints.append("ability: "+ability)

  #saves the name of the pokemon to the current instance of the game
  ng.pokemon=name
  return hints

#Using the set difficulty, reads the pokemon image file and outputs an ascii interpretation.
#The number of columns used to generate the image will change depending on the difficulty.
def displayPokemon(difficulty):
  my_art = AsciiArt.from_image('pokemon.png')
  columns= 30
  if difficulty == 3:
    columns = 30
  elif difficulty == 2:
    columns = 50
  elif difficulty == 1:
    columns = 75
  my_art.to_terminal(columns)

#Using the current game instance and a task input, will handle account creation and updates.
#A list of player data is saved to the [playerData.json] file or create one if non exists.
def handleAccount(ng, task):
  if (task=="sign_in"): #Perform sign in or account creation tasks
    if os.path.exists("playerData.json"): # Check if [playerData] exists
      with open("playerData.json", "r") as file: #read file and save contents to playerList
        playerList = json.load(file)
      print("Please type in your name and password to save your score. If you dont have one a new one will be created.")
      #Return a dict with all of the player's saved info or create a new player.
      while (True): 
        name=input("name :: ")
        password=input("password :: ")
        player={"name":name, "password":password, "score":0}
        for i in range(0,len(playerList)):
          if name == playerList[i]["name"]: #Looks for the player in the database
            if password == playerList[i]["password"]: #Checks they input the correct password
              return playerList[i]
            else:
              print("Incorrect password for that name. Try Again.")
              break
          elif i==len(playerList)-1: #Adds a new player to the database if the [name] does not exist
            playerList.append(player)
            with open("playerData.json", "w") as file:
              json.dump(playerList, file)
            return player
    else: 
      #Execute the same as above but create a [playerData.json] file 
      #with the first entry being the current player
      print("Please type in a name and password to save your score.")
      name=input("name :: ")
      password=input("password :: ")
      player = {"name":name, "password":password, "score":0}
      playerList = [player]
      with open("playerData.json", "w") as file:
        json.dump(playerList, file)
      return player

  #perform account update tasks within the [playerData.json] file
  if(task=="update"):
    with open("playerData.json", "r") as file:
        playerList = json.load(file)
    #iterate through the database and update the players score if the current score is greater.
    for i in range(0,len(playerList)):
      if(playerList[i]["name"]==ng.player["name"]):
        if(playerList[i]["score"]<ng.score):
          playerList[i]["score"]=ng.score
          break
        break
    with open("playerData.json", "w") as file:
        json.dump(playerList, file)

#Display a running list of High Scores saved in the [playerData.json] file
def scoreValue(e):
  return e["score"] #used to sort the list of player scores
def highScore():
  with open("playerData.json", "r") as file:
    playerList = json.load(file)
  playerList.sort(reverse=True,key=scoreValue) #sort the values in reverse order
  #stylize and print the scores to the terminal
  print("----HIGH SCORES----")
  print("|  NAME : SCORE   |")
  for player in playerList: #print the name and score of each player
    #make sure that the name is max 6 letters and fills in the leftover space
    scoreName=""
    count=0
    for letter in player["name"]:
      count+=1
      if count <=6:
        scoreName+=letter
    scoreName+=" "*(6-count)
    #make sure that the score fills in the leftover space 
    #!*[COMEBACK AND FIX FOR VERY HIGH SCORES]*!
    scoreScore=str(player["score"])
    count=0
    for number in scoreScore:
      count+=1
    scoreScore+=" "*(6-count)
    print("|"+scoreName+" :   "+scoreScore+"|")
  print("-"*19)  
  
#GAME START -------------------------------------------------------------------------------------
intro() #intro text displaying rules and instructions
ng=NewGame() #create a new instance of the Game with various initial values
#create/load a player dict with a [name] [password] and [score] and set it to the current instance
player=handleAccount(ng, "sign_in") 
ng.player=player
print("Hello "+player["name"])
difficulty = setDiff()
hints = generatePokemon(ng)
displayPokemon(difficulty)

#Loop that always comes back to the input [prompt] after all input checks are made.
#each if statement will run it's code if the player types the correct response.
while(True):
  prompt=input(":: ")
  if(prompt=="manual"):
    rules()
  elif(prompt=="pokemon"):
    displayPokemon(difficulty)
  elif(prompt=="hint"): #show a random hint, but decrease the number of available hints.
    if(len(hints)>0 and ng.hintNumber>0):
      randomNum = random.randint(0, len(hints)-1)
      print(hints.pop(randomNum))
      ng.hintNumber=ng.hintNumber-1
    else:
      print("Sorry, you have used up all your hints.")
  elif(prompt=="score"): #print current score and amount of hints available
    print(f"Score: {ng.score} | Hints: {ng.hintNumber}")
  elif(prompt=="restart"): #run all of the initializing lines of code from the GAME START
    intro()
    ng=NewGame()
    player=handleAccount(ng, "sign_in") 
    ng.player=player
    print("Hello "+player["name"])
    difficulty = setDiff()
    hints = generatePokemon(ng)
    displayPokemon(difficulty)

  #adds a second layer of prompts for the guess so the player doesn't use up a guess by mistake.
  elif(prompt == "guess"): 
    guess= input("Type your guess:: ")
    #generate a new pokemon if guessed correctly and add 100 points to the players current score
    if(guess == ng.pokemon):
      ng.score+=100
      print(f"You guessed {ng.pokemon} correctly! +100p")
      ng.tries=3
      hints = generatePokemon(ng)
      displayPokemon(difficulty)
    #Decrease the number of tries if the player guesses wrong 
    #and decrease their current score by 25 points.
    #If the player uses up all of their tries, will update their account and provide ending prompts.
    else: 
      ng.score-=25
      if(ng.tries>1): 
        ng.tries-=1
        print("Sorry incorrect guess. -25p")
      else:
        print("GAME OVER! Sorry, you have used up all your tries.")
        print(f"Score:{ng.score}")
        handleAccount(ng, "update")
        print("Type [restart] to play again, [high score] to see the leaderboard, and [exit] to close the game.")
        while(True):
          prompt=input(":: ")
          if(prompt=="restart"): # RESTART GAME
            ng=NewGame()
            player=handleAccount(ng, "sign_in") 
            ng.player=player
            print("Hello "+player["name"])
            difficulty = setDiff()
            hints = generatePokemon(ng)
            displayPokemon(difficulty)
            break
          elif(prompt=="high score"): # DISPLAY HIGH SCORES
            highScore()
          elif(prompt=="exit"): # END GAME
            print("bye!")
            sys.exit()


