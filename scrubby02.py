import rg

class Robot:
    def act(self, game):
        # if we're in the center, stay put
        if self.location == rg.CENTER_POINT:
            return ['guard']

        # if there are enemies around, attack them
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    if self.hp <= 2:
                        return ['suicide']
                    else:
                        return ['attack', loc]

        # move toward the center if we are not blocked. If we are, guard.
        moveToPoint = rg.toward(self.location, rg.CENTER_POINT)

        if 'obstical' in rg.loc_types(moveToPoint):
            return ['guard']
        else:
            return ['move', moveToPoint]