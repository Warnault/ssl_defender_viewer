import numpy
import sys

from goal import *

from enum import Enum

class ShotResult(Enum):
    GOAL = 1
    INTERCEPTED = 2
    OUT = 3

class Shot:
    """
    src : np.array(2,)
        Source of the shot in field referential
    end : np.array(2,) or None
        Ball position at the end of the shot, None if ball does not encounter
        any obstacle or the goal
    result : ShotResult
        The result of the kick after the shot
    """
    def __init__(self, src, end, result):
        self.src = src
        self.end = end
        self.result = result


class Problem:
    def __init__(self, data):
        # Checking cont
        mandatory_keys = ["field_limits", "robot_radius",
                          "opponents", "theta_step", "pos_step", "goals"]
        for key in mandatory_keys:
            if key not in data:
                raise ValueError("Cannot find '" + key + "'")
        # Reading field limits
        self.field_limits = numpy.array(data["field_limits"])
        if (self.field_limits.shape != (2, 2)):
            raise ValueError("Invalid shape for 'field_limits': "
                             + str(self.field_limits.shape) + " expecting (2, 2)")
        # Reading goals
        self.goals = []
        for goal_data in data["goals"]:
            self.goals.append(Goal(goal_data))
        if (len(self.goals) == 0):
            raise ValueError("No goal found")
        # Reading opponents
        self.opponents = numpy.array(data["opponents"]).transpose()
        if (self.opponents.shape[1] == 0):
            raise ValueError("No opponent found")
        if (self.opponents.shape[0] != 2):
            raise ValueError("Invalid data for opponents")
        # Reading other parameters
        self.robot_radius = data["robot_radius"]
        self.theta_step = data["theta_step"]
        self.pos_step = data["pos_step"]
        # Reading optional parameters
        self.defenders = None
        if "defenders" in data:
            self.defenders = numpy.array(data["defenders"]).transpose()
        # Reading optional minimal distance
        self.min_dist = None
        if "min_dist" in data:
            self.min_dist = data["min_dist"]
        # Reading optional goal area
        self.goalkeeper_area = None
        if "goalkeeper_area" in data:
            self.goalkeeper_area = numpy.array(data["goalkeeper_area"])
            if self.goalkeeper_area.shape != (2,2):
                raise ValueError("Invalid shape for 'goalkeeper_area': "
                                 + str(self.goalkeeper_area.shape)
                                 + " expecting (2, 2)")
            for dim in range(self.goalkeeper_area.shape[0]):
                dim_min = self.goalkeeper_area[dim,0]
                dim_max = self.goalkeeper_area[dim,1]
                if dim_min >= dim_max:
                    raise ValueError("Invalid data for goalkeeper_area along"
                                     "dim {:}, min >= max ({:} >= {:}".format(
                                         dim, dim_min, dim_max))
        # Reading optional ball_max_speed and robot_max_speed
        self.ball_max_speed = data.get("ball_max_speed")
        self.robot_max_speed = data.get("robot_max_speed")
        has_bms = self.ball_max_speed is not None
        has_rms = self.robot_max_speed is not None
        if has_bms ^ has_rms:
            raise ValueError("Ball max speed and robot max speed should appear "
                             "both or None")

    def getFieldCenter(self):
        """ Return the position of the center of the field """
        return (self.field_limits[:, 1] + self.field_limits[:, 0]) / 2

    """ Width of the playing field [m]"""

    def getFieldWidth(self):
        return self.field_limits[0, 1] - self.field_limits[0, 0]

    """ Height of the playing field [m]"""

    def getFieldHeight(self):
        return self.field_limits[1, 1] - self.field_limits[1, 0]

    def getNbOpponents(self):
        return self.opponents.shape[1]

    def getOpponent(self, opp_id):
        return self.opponents[:, opp_id]

    def getNbDefenders(self):
        if (self.defenders is None):
            return 0
        return self.defenders.shape[1]

    def getDefender(self, def_id):
        return self.defenders[:, def_id]


    def computeShotResult(self, src, kick_dir, defenders):
        # Getting closest goal to score
        kick_end = None
        best_dist = None
        for goal in self.goals:
            kick_result = goal.kickResult(src, kick_dir)
            if not kick_result is None:
                goal_dist = numpy.linalg.norm(src - kick_result)
                if best_dist == None or goal_dist < best_dist:
                    best_dist = goal_dist
                    kick_end = kick_result
        if kick_end is None:
            return Shot(src, None, ShotResult.OUT)
        # Checking if kick is intercepted by one of the opponent and which one is the first
        result = ShotResult.GOAL
        for def_id in range(defenders.shape[1]):
            defender = defenders[:, def_id]
            if self.ball_max_speed is not None:
                collide_point = segmentPointProjection(src, kick_end, defender)
                robot_dist = np.linalg.norm(collide_point - defender) - self.robot_radius
                robot_time = robot_dist / self.robot_max_speed
                ball_time = np.linalg.norm(collide_point - src) / self.ball_max_speed
                if ball_time < robot_time:
                    collide_point = None
            else:
                collide_point = segmentCircleIntersection(
                    src, kick_end, defender, self.robot_radius)
            if not collide_point is None:
                kick_end = collide_point
                result = ShotResult.INTERCEPTED
        return Shot(src, kick_end, result)

    def computeShotsResults(self, defenders, filter_out = True):
        shots = []
        for opp_id in range(self.getNbOpponents()):
            kick_dir = 0
            while kick_dir < 2 * math.pi:
                s = self.computeShotResult(self.getOpponent(opp_id), kick_dir,
                                           defenders)
                if s.result != ShotResult.OUT or not filter_out:
                    shots.append(s)
                kick_dir += self.theta_step
        return shots
