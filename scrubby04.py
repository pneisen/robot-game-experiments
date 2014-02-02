import rg
import random

class Robot:
    rallyPoint = random.choice([(6,6), (12,6), (7,11), (8, 14)])

    currentTurn = -1;
    numberOfFoes = 0;
    numberOfFriends = 0;

    def updateVariables(self, game):
        self.numberOfFoes = 0;
        self.numberOfFriends = 0;

        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                self.numberOfFoes += 1
            else:
                self.numberOfFriends += 1

    def attackOrSuicide(self, locToAttack, botToAttack):
        if self.hp <= 11 and botToAttack.hp <= 15:
            return ['suicide']
        else:
            return ['attack', locToAttack]

    def act(self, game):
        # Update the class variables if this is a new turn. 
        if game.turn != self.currentTurn:
            # If this is the very first turn, print out some info.
            if game.turn == 1:
                print "The rally point is: {0}".format(self.rallyPoint);

            self.updateVariables(game);
            self.currentTurn = game.turn;
            print "New Turn! " + str(self.currentTurn) + " Friends: " + str(self.numberOfFriends) + " Foes: " + str(self.numberOfFoes);

        # First order of business, if this bot is on a spawn point, we need to get him out of there. 
        if 'spawn' in rg.loc_types(self.location):
            # Try to move toward the rally point.
            moveToPoint = rg.toward(self.location, self.rallyPoint);
            if 'normal' in rg.loc_types(moveToPoint):
                return ['move', moveToPoint];
            else:
                # Can't move towards the rally point. See where we can move. 
                adjacentLocations = rg.locs_around(self.location);
                for loc in adjacentLocations:
                    if 'normal' in rg.loc_types(loc):
                        return ['move', loc];

                # If we got here, we can't move off the spawn point. Let's try to do some damage if we have a nearby enemy. 
                for loc in adjacentLocations:
                    if loc in game.robots:
                        if game.robots[loc].player_id != self.player_id:
                            return self.attackOrSuicide(loc, game.robots[loc]);

                # If we are here, nothing else we can do, but guard. We must be blocked by our guys. Hopefully they will get out of the way.
                return ['guard'];


        # Now some strategy. 
        if self.numberOfFoes > self.numberOfFriends:
            # We have less bots than the enemy. Let's play it safe until the numbers are back in our favor.
            
            # Head to the rally point if possible. Fight if someone gets in the way, but be passive otherwise. 
            if (self.location == self.rallyPoint):
                return ['guard'];

            moveToPoint = rg.toward(self.location, self.rallyPoint);
            if 'normal' in rg.loc_types(moveToPoint):
                return ['move', moveToPoint];
            else:
                # We can't move. Attack if we can.
                for loc in adjacentLocations:
                    if loc in game.robots:
                        if game.robots[loc].player_id != self.player_id:
                            return self.attackOrSuicide(loc, game.robots[loc]);

            # Guard if we can't move.                     
            return ['guard'];
        
        else:
            # We have the numbers advantage. Start hunting. 
            return ['guard'];

