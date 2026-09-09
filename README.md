# This readme is mostly for prospective employers

We will first go over the structure and content of the repo, then we will proceed with the reasoning behind the key decisions for our workflow, and further down we will explain how to use it.

## Structure & Contents


| Folder | Content | Attribution |
|----------|:-------------:|------:|
| Books | This folder contains the working version of the rulebook and the storybook. The beginner guide and handout are currently unfinished. All books are written in LaTeX. | A.M. & A.V. |
| Pictures | All of the icons and pictures we use in the game. The pictures we use in the books only are located in the Books folder | A.V. |
| Races | This folder name may seem off-putting if you are not into fantasy games. Races simply used to be the normal term for the collection of different species. Think Elves, Dwarves, Fae etc... The folder contains the files with our domain specific language which define the cards we print for our playable races (called ancestries in the rules) | A.M. & A.V. |
| Classes | Same a Races, but less unfortunately named | AM & AV |
| ToPdfPipeline | This contains all of the python infrastructure we need to generate nanDECK code from the files in the folders Races & Classes and the files MonsterAI, Stories_Encounters & Events.csv | AM |
| Comms | Here you can find (non-confidential) communication with various parties, mostly the Spielauthorenzunft and Publishers | A.M. & A.V. |
| Math | This folder contains an orphaned combat simulator. As it turned out, balancing isn't that important | A.M. |

| Single Files | Content | Attribution |
|----------|:-------------:|------:|
| Events & EventIdeas | The finished and unfinished events for our game | A.M. & A.V. |
| Ideas & ToDoList | Tracker files to jot down what we need, should or might do in the future | A.M. & A.V. |
| Monster AI & Storeies_Encounters | Definitions for the games enemies and how they are set up when playing | A.M. & A.V. |
| webcrawler.py | We needed to try really hard to get into the Spieleauthorentreffen in Göttingen. Please never tell anyone we did this | A.M. |
| WheelOfElements.ods | We use this file to track all of the high-level decisions about the balance and structure of the game | A.M. & A.V. |
| Monument.ods | A sheet with our discarded Ideas, and a reminder of how far we came | A.V. |

## Workflow decisions

Most of our decisions are affected by our team size (2) and the fact that we are doing this without outside pressure since this project is a hobby.

### Branching strategy
In the industry it is commonplace to collaborate using feature branches and pull requests to maintain a clean and workable master.
Since we are two people and we can very easily communicate about who does what when, we really don’t run into conflicts enough to warrant more than a main.
When necessary we can roll our version back to reach a stable state. This has been done about once in three Years.

In the coming weeks we will make a stable branch for others to cgeck out.

### Folder structure
We usually group stuff near the top level and by semantic proximity, even if the contents are meant to work in tandem across folders, like the Pdf Pipeline works with Pictures, Races & Classes.
This has generally been sufficient. When the chaos grows too much we do clean up. You may find some orphaned and deprecated files in the repo. Usually we keep those that we want to keep somewhat fresh in memory.
There are also quite a few loose files on the top level. Most of them come in pairs and it felt unwarranted to put them into their own folder.

### AI usage
Nearly none of this is AI generated, with the exception of the web crawler. 
Since we are producing art as a hobby in here, we made the decision to take the time and learn new skills when necessary and to craft the game experience by hand hand with love and intent.

### Work times
Generally we manual work (coding, writing etc.) on Saturdays fom 12-14. We have kept this up for around three years now, and the cumulative progress can really be felt.
Apart from that we have many design discussions during lunchtime and after we play other games.
There are also hot phases leading up to conventions and play-tests outside of our core group. 
This results in higher workloads that we get done whenever possible. 
We roughly plan at the start of a hot phase what we can get done in the time frame and then when we get there we usually squeeze in some extra.

### Coding Guideline
Since I (A.M.) am working on the python and nanDECK code by myself I lucky don't have to align with others.
Unfortunately, this doe not relieve me from aligning with myself. 

**Function names** - I try to keep all functions that do similar stuff also named similar. Example "sliceClassToCardTypes(lines)" and "sliceStatsToCards(lines)". 
Both of these functions separate a number of lines int semantic units for further processing.

**Variable names** - Variables normally take the form of [Type][Name]. 
I know that type hints exist in python, but this is a hassle free way of essentially naming structs with boring definitions. 
For example, "lines" refers to list of Strings and is the main way I handle and iterate over text.

**File contents** - The code is split into a Parser and Card definitions.
The parser does all of the logic, and the Card definitions exist separately to externalise knowledge about how the result should look like.
Having the Cards as their own classes helps to keep knowledge about how the cards need to be processed further self-contained and modular. 
This approach significantly helped when making the switch from LaTeX to nanDECK as our engine to convert code to printable cards.

**Code generation** - The code generation itself is strongly aided by templates, which I use in conjunction with simple text replacement.
I started with this approach before templates were native to python and more powerful solutions like jinja are overkill for this project.

## How to use

If you actually take the time to look at this stuff, please write me any feedback you may have at ainfomail@arcor.de

### Books
The rulebook is written in LaTeX, and can be compiled like any normal LaTeX document. You may need to download some extra packages
Currently the rulebook is lagging behind the actual game files, and we plan to update this in two weeks.

### ToPdfPipeline
In this step we go from our domain specific language to code that can pe processed into pictures.
The main file to execute is ToPdfPipeline/Parser_WheelOfFate.py
This will read the MonsterAI, Stories, Events and all files in Races & Classes to generate code for a third party software named nanDECK.
the resulting code is placed in ToPdfPipeline/out/.

If some files are not generated, you may have to comment the corresponding function in. The relevant code can be found all the way at the bottom in the Parser.

Our only dependency is pandas.

### nanDECK files to pdf's

This step needs the third party software [nanDECK](https://nandeck.com/).
All of the text files you have created can be found in ToPdfPipeline/out/.

For how to use nanDECK, please refer to the official documentation on heir website.
YouTube tutorials are also pretty good for this.
You will need to change your settings (at the bottom left) and set the comment character to #.
Afterwards you can validate and build the decks.
nanDECK then offers various options for printing. 
Usually we print directly or we convert the output to a pdf and print that.

There are also some custom nenDECK files in ToPdfPipeline/CustomCards/ which you can build and print separately.

### Assembly

For our prototypes, we use 3D printed tableaus and class tiles,but the stl files are not part of this repo.
We recommend assembling the resulting cards as close as possible to the pictures you can find in the rulebook.
You will also need a good bunch of cubes dice, and other material to actually play.
To assemble physical objects, like the custom dice we recommend using sticky & printable paper.

If you are missing any explanation, contact me at ainfomail@arcor.de
