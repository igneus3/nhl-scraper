class Player():
    def __init__(self, playerId: int):
        self.playerId = playerId

        self.assists = 0
        self.blocked_shots = 0
        self.faceoff_wins = 0
        self.faceoffs = 0
        self.giveaways = 0
        self.goals = 0
        self.hits_given = 0
        self.hits_received = 0
        self.missed_shots = 0
        self.penalties_committed = 0
        self.penalties_drawn = 0
        self.penalties_served = 0
        self.primary_assists = 0
        self.secondary_assists = 0
        self.shots = 0
        self.shots_on_goal = 0
        self.so_failed_shot = 0
        self.so_shots = 0
        self.takeaways = 0

    def call(self, name):
        if hasattr(self, name) and callable(func := getattr(self, name)):
            func()

    def add_faceoff_win(self):
        self.faceoffs += 1
        self.faceoff_wins += 1

    def add_faceoff_loss(self):
        self.faceoffs += 1

    def add_goal(self):
        self.shots += 1
        self.shots_on_goal += 1
        self.goals += 1

    def add_shot_on_goal(self):
        self.shots += 1
        self.shots_on_goal += 1

    def add_missed_shot(self):
        self.shots += 1
        self.missed_shots += 1

    def add_takeaway(self):
        self.takeaways += 1

    def add_giveaway(self):
        self.giveaways += 1

    def add_penalty_committed(self):
        self.penalties_committed += 1

    def add_penalty_drawn(self):
        self.penalties_drawn += 1

    def add_penalty_served(self):
        self.penalties_served += 1

    def add_blocked_shot(self):
        self.blocked_shots += 1

    def add_shot(self):
        self.shots += 1

    def add_hit_given(self):
        self.hits_given += 1

    def add_hit_received(self):
        self.hits_received += 1

    def add_primary_assist(self):
        self.assists += 1
        self.primary_assists += 1

    def add_secondary_assist(self):
        self.assists += 1
        self.secondary_assists += 1

    def add_so_failed_shot(self):
        self.so_shots += 1
        self.so_failed_shot += 1

