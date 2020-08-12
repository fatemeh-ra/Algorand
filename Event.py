

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
