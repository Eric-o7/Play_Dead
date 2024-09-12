#This module will be used to store variables for the typing animation function so that the main.py module does not get cluttered.
import main

feast = f'''    After the feast, Kesk says to you, "Now go get some rest, {main.player.name}. Tomorrow we begin planning our ascent in the food chain."

Later that day, while the passel slept. You wake up to the hissing of snakes near the oak grove. 

As you poke your head out of the hollow, you see Elpos with a claw hammer slung over his shoulder talking to a larger than normal timber rattlesnake.

Elpos senses you, looks over and smirks...

"This unnatural formation and rise of opossums is heresy, {main.player.name}! Snakey and I have been charged with maintaining order in these mountains. You and Kesk will regret seeking your unnatural gifts." 

"Prepare for battle!"

Enter OK to continue.
___________________\n'''

post_grove_battle = f'''    After the battle, you see that Kesk was injured and some of the passel has been killed.
Kesk calls you into his hollow where he is tending his wounds.
"{main.player.name}, YOU must avenge this disgraceful attack.
Go back up the winding path towards the mountain bald and see if you can find a vantage point to track Elpos.
The other 'possums of the passel need to stay behind to defend the grove in case of another attack.

On your journey, be on the lookout for three things:
1. How can we defend our grove?
2. Where did Elpos get his powers?
3. Where can we recruit allies to help our cause?

Get some rest and start your journey at nightfall."

Would you like to speak to other members of the passel before you leave?\n'''

speak_to_passel = f'''  You talk to the matron of the grove first. 
She says "My dear {main.player.name} - you fought to protect this grove and your new gifts.
You must know that Kesk is hurt very badly.
He wants you to look for allies. When you find new allies, make sure you tell them that we have food and shelter here at the grove.
We all have faith in you, {main.player.name}."

Next you talk to the lorekeeper of the grove, who is hanging upside down from a nearby treebranch waving in the breeze. Her eyes are closed.
"Pay attention, young 'possum. When you are looking for friends, keep in mind that other creatures in these mountains also "play dead" when threatened.
They may be sympathetic to our cause."

Enter OK to continue.
_____________________
'''

path_1 = f'''   At nightfall, you gather your things, cross the creek near the Oak Grove, and find the winding path.

The path that you were just on last night. The path that leads to the fern cave where the fairy ring was. The path that leads to the bald mountain top.

As the sun sets, and your vision adjusts, you see a fox from afar laying down behind some brush.

You blink and the fox is gone.

You continue your hike upwards, and you see the path split to your left. That is the way to the fern cave.

Would you like to keep going UP the path, or wander into the fern CAVE?\n'''



fern_cave_1 = f'''  As you enter the Fern Cave, you see the mushrooms that once made up the Fairy Ring are wilting. You sense a surge of humidity in the cave, the air feels thick with moisture. In front of you in the darkness you make out a mushroom shape object. The mushroom has a red cap with white spots. It turns around and greets you.

"Hello young 'possum. I am Amanita. I have come to recycle this fairy ring into the earth, lest it be used maliciously by uninvited participants."

"What do you mean?" you ask. 

"There are strange things happening in the mountains recently. I have heard news of other kinds of rings appearing, rings that have not been sanctioned by the fairies of Appalachia. There has been an imbalance that, if continued unabated, would throw the ecological dependencies of this region into chaos."

You confusingly ask, "Am I part of that imbalance?"

Amanita looks to the side, continuing their work to reclaim the energy.

"In some ways, yes you are. Though imbalances are not caused by novel abilities and community building, rather by willful and deceitful actions of those who wish to hinder or obstruct change. Thereby, you are not the cause of such an imbalance, but you are not without cause."

Respond with 'OK' to nod and walk away or 'what the HELL are you talking about?' to learn more.\n)'''
 
fern_cave_2 = f'''" I am speaking to the nature of our existence in such a world. By existing, you push and pull the chains of balance against other such actors. Take your appetite for ticks for example. Though you engorge on the little bugs at will, if too many are removed, the ripples of change would affect nearly every living creature. 

Some factions, like the one I associate with, champion change sufficient for one species but not in a way that outdoes or pushes away the dependencies of that species and the others that rely on it. We have reviewed some potential outcomes of our interjection here. The consequences are mostly benign, yet they do exist. You're quite lucky. Your father, Kesk, found and convinced us to help restore dignity to the Opossum. Before now, we have not acted in this world since the Dinosaurs roamed these mountains."

Amanita looks directly at you.

"Yet, now that we have, our overlords have seen to it to test your new abilities. Though you're lucky, you're also hunted. You are to be the subject of tests both directly and indirectly, and your actions will be monitored closely. Do not betray our trust or disappoint our support for your species." 

"I'll do my best!" you exclaim with hesitation.

"The world is better with you in it, {main.player.name}. Continue to fight for your passel, and for your father. 

By the way, if you see any fairy rings that are comprised of mushrooms that look like me, you can attempt to destroy them. I know that paints me in a suspicious light, but remember... it's all part of the balance."

You nod to Amanita, and make your way out of the shallow cave. The comforting glow of moonlight fills you with hope.

Enter OK to continue.
_____________________'''

fox_1 = f'''    You keep walking up the winding path. You hear leaves crunching behind you, you look back and you see the fox from before.

"Look at you little 'possum." The fox says slyly.

"You aren't going to run or play dead? You think you're safe walking on this path alone now? What is that you're holding? Weapons?"

You straighten up, look at the fox squarely and share "I'm walking a new path now, fox. I'm done playing dead."

Fox squints and looks you once over. "Well here's the thing little 'possum... my pups need to eat and you would make a good meal."

Respond with "COME and get it then!" or "I can HELP with food!"\n"'''

fox_2 = f'''    "I don't need any help from a 'possum. You ARE food... but then again I am confused by what you now have become..."

Respond with "COME see for yourself then!" to fight, "Ok SUIT yourself" to start walking away, or "We HAVE food" to continue the conversation.'''

help_fox = f''' Look, we have food that we have gathered in the Oak Grove just down the path and across the creek. Tell them {main.player.name} invited you to our grove and they will help."

You look down as you feel slightly embarassment at the food stores you know are available. "This food came from preparation and working together, something us 'possums have not done well at until recently."

"We are recovering from an ambush but I don't want you to go hungry. Please go see for yourself."

The pensive fox raises his eyebrowns and looks at you closer than ever before, as if he is trying to see through you to a different reality. The fox blinks...

"Maybe I will then... I'll go see what's going on... Things sure are changing around here."

Enter OK to continue.
_____________________'''

path_3 = f'''   You continue your journey up the winding path. The path is well lit thanks to a clear sky. There are moths dancing in the moonlight, spiders sitting in webs awaiting their meal, and tracks on the path that look like a snake has recently traveled this way. You start to feel the gravity of the situation as you hike the path. Your place in nature as an opossum is confusing but unique. Why and how have I gotten into this? Was my father right in his effort to bring opossums together?

As you go deeper in your thoughts, and higher up the mountain, you see another fork in the path. You know this is the off-shoot to the maple cave. You see the large maple tree in the distance that stands next to the cave entrance. The maple cave is large enough for a black bear to make a den out of it. In the past, opossums that you know have not typically wandered into that part of the cave.

Do you continue to the mountain top BALD or go to the maple CAVE?'''

maple_cave = f'''   As you veer off the winding path into the light brush of the forest toward the Maple Cave, the moonlight gets dimmer.

You come to the entrance of the Maple Cave very carefully. You peak inside, and you see a small circle of mushrooms on the ground. 

These mushrooms look different than the ones that made up the fairy ring you walked into last night. They are red with yellow spots. 

You feel an emanation of chaos coming from them.

Would you like to ENTER the ring, DESTROY the mushrooms, or LEAVE immediately?'''

enter_maple_ring = f''' You enter a state of trance. Your mind goes blank and you see nothing but darkness. In that darkness, a light appears in the distance. It slowly grows in size as it seems to get closer to you. In that light you start to make out a vision. You see the Oak Grove but it's empty. You see no other Opossums there, not even Kesk. 

The vision pans out and you see a group of opossums in the creek. They're laying belly up. One of them is Kesk. A vulture crashes down into the shallow creek, perching on a stone, it rips at the body of Kesk. The vision ends. The cave shakes from above as you return to your senses.

The rumble quiets, and you see tendrils stretch across the mouth of the cave. From the shadows cast by the moonlight you see a silhouette of a Venus Flytrap. It lunges at you!

Enter OK to continue.
_____________________'''

stomp_maple = f'''  You stomp on the mushrooms. As you feel the red yellow-spotted fruiting bodies squish below your paws, your bones shake from a rumble in the dirt, and a growl from above...

The rumble quiets, and you see tendrils stretch across the mouth of the cave. From the shadows cast by the moonlight you see a silhouette of a Venus Flytrap. It lunges at you!

Enter OK to continue.
_____________________''' 

leave_cave = f'''   You run out of the cave. As the moon illuminates your fur, you feel a tingling in the back of your neck. You turn around and look above the cave to see a giant Venus Flytrap that has sprouted tendrils and is reaching for you.

Would you like to RUN or FIGHT?'''

after_venus_combat = f'''   The Venus Flytrap screeches. Bugs and carrion spew from its mouths. You step aside as it withers and dies. Well fought, {main.player.name}!

Enter OK to continue.
_____________________'''

past_maple_cave = f'''  You resume your journey up the winding path. With a few hours left until dawn, you start to reach the top of the mountain. 

The path fans out in all directions and disappears into the bald top of the mountain. You see a snake skin on the side of one of the paths.

Would you like to INVESTIGATE the snake skin or keep going UP toward the center of the mountain top?'''

investigate_snake = f'''    You get on all fours and sniff at the snakeskin. It smells different than the snakes that attacked the grove. 

Your eyes squint and you see a snake in the brush nearby roll over, it's white belly up to the moon. The snake looks to be playing dead.

As you approach you see a few nearby snakes raise their head out of the brush and tall grass on the perimeter of the mountain top. The snake heads have an upturned snout that looks like a pig's nose.

The snake that was playing dead rolls over.

"You er not like the other 'possummsss around 'ere"
"We are not enemiesss" says a snake from the tall grass.

"What are you?" you ask.

"Weeee are the hognosesss. Our kind playss dead like you." The former thanatosed snake says to you. 

You think to yourself... maybe this is the kind of ally the grove lorekeeper was talking about. You've heard of your kind eating hognose snakes, but you didn't know they played dead like you. Will nature rebalance in a way that makes hognoses our allies?

The snakes watch as you consider the situation. 

