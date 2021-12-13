

class Event(object):
    def __init__(self, refTime, eventTime, eventType, msg, timeOut, targetNode, sourceNode, roundNumber, stepNumber):
        self.Ref_Time = refTime
        self.Event_Time = eventTime
        self.Event_Type = eventType
        self.Msg_To_Deliver = msg
        self.Time_Out = timeOut
        self.Target_Node = targetNode
        self.Source_Node = sourceNode
        self.Round_Number = roundNumber
        self.Step_Number = stepNumber

    def __lt__(self, other):
        return self.Event_Time < other.Event_Time

    def __str__(self):
        return "Event Time : " + str(self.Event_Time) + " Event Type: " + str(self.Event_Type) + " Message: " + \
               str(self.Msg_To_Deliver) + "from " + str(self.Source_Node) + " to " + str(self.Target_Node)

