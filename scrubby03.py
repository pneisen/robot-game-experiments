import rg

class Robot:
    def act(self, game):
        # Attack nearby robots. Suicide if we are low on health.
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    if self.hp <= 11 and bot.hp <= 15:
                        return ['suicide']
                    else:
                        return ['attack', loc]

        # Find the nearest enemy bot and move towards it if we can. Otherwise head to the center.
        distanceToEnemy = 50
        enemyLocation = rg.CENTER_POINT

        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                distance = rg.dist(loc, self.location)
                if distanceToEnemy > distance:
                    distanceToEnemy = distance
                    enemyLocation = loc

        moveToPoint = rg.toward(self.location, loc)

        if moveToPoint == self.location:
            return ['guard']

        if 'normal' in rg.loc_types(moveToPoint):
            return ['move', moveToPoint]
        else:
            return ['guard']
