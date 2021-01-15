# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit


from random import randrange


class generator:
    def __init__(self, kpnGraph, platform, mappingIdentifier=[]):
        self._peIdentfier = []
        self._taskIdentfier = []
        self._mappingIdentifier = mappingIdentifier

        for pe in platform.processors():
            self._peIdentfier.append(pe.name)
        for task in kpnGraph.processes():
            self._taskIdentfier.append(task.name)

    def generateQuery(self, length, depth=0):
        result = "EXISTS " + self._generateQuery(length, depth + 1)
        return result

    def _generateQuery(self, length, depth):
        result = ""
        if depth == 1:
            usedIdentifier = []
            usedRunningTogether = []
            relation = randrange(2)
            for i in range(0, length):
                if self._mappingIdentifier == []:
                    operation = randrange(3)
                    if operation == 0:
                        mappingOp = self._MappingOperation(usedIdentifier)
                        result += mappingOp[0]
                        usedIdentifier.append(mappingOp[1])
                    elif operation == 1:
                        tmp = self._SharedCoreOperation(
                            usedRunningTogether, usedRunningTogether
                        )
                        result += tmp[0]
                        for element in tmp[1]:
                            usedRunningTogether.append(element)
                    else:
                        result += self._ProcessingOperation()
                else:
                    operation = randrange(10)
                    if operation < 3:
                        mappingOp = self._MappingOperation(usedIdentifier)
                        result += mappingOp[0]
                        usedIdentifier.append(mappingOp[1])
                    elif operation >= 3 and operation < 6:
                        tmp = self._SharedCoreOperation(
                            usedRunningTogether, usedRunningTogether
                        )
                        result += tmp[0]
                        for element in tmp[1]:
                            usedRunningTogether.append(element)
                    elif operation == 9:
                        result += self._EquivalentOperation()
                    else:
                        result += self._ProcessingOperation()
                if i < length - 1:
                    if relation == 0:
                        result += " AND "
                    else:
                        result += " OR "

        else:
            result += "( " + self._generateQuery(length, depth - 1) + " ) "
            rnd = randrange(2)
            if rnd == 0:
                result += "AND"
            else:
                result += "OR"

            result += " ( " + self._generateQuery(length, depth - 1) + " )"

        return result

    def _MappingOperation(self, usedIdentifier):
        result = ""
        rnd = randrange(2)
        negated = False
        if rnd == 1:
            result = "NOT "
            negated = True

        rnd = randrange(0, len(self._taskIdentfier))
        taskIdentifier = self._taskIdentfier[rnd]
        while taskIdentifier in usedIdentifier:
            rnd = randrange(0, len(self._taskIdentfier))
            taskIdentifier = self._taskIdentfier[rnd]

        rnd = randrange(0, len(self._peIdentfier))
        peIdentifier = self._peIdentfier[rnd]
        if negated:
            while peIdentifier == "ARM00":
                rnd = randrange(0, len(self._peIdentfier))
                peIdentifier = self._peIdentfier[rnd]

        result += taskIdentifier + " MAPPED " + peIdentifier

        return (result, taskIdentifier)

    def _ProcessingOperation(self):
        result = ""
        rnd = randrange(4)
        negated = False
        if rnd != 1:
            result = "NOT "
            negated = True
        rnd = randrange(0, len(self._peIdentfier))
        peIdentifier = self._peIdentfier[rnd]
        if negated:
            while peIdentifier == "ARM00":
                rnd = randrange(0, len(self._peIdentfier))
                peIdentifier = self._peIdentfier[rnd]

        result += peIdentifier + " PROCESSING"

        return result

    def _SharedCoreOperation(self, usedIdentifier, usedRunningTogether):
        result = ""
        currentlyUsed = []

        rnd = randrange(2)
        if rnd != 1:
            result = "NOT "
        result += "RUNNING TOGETHER ["

        rnd = randrange(0, len(self._peIdentfier))
        taskIdentifier = self._taskIdentfier[rnd]
        i = 0
        while taskIdentifier in usedRunningTogether:
            rnd = randrange(0, len(self._peIdentfier))
            taskIdentifier = self._taskIdentfier[rnd]
            i += 1
            if i > 20:
                return self._MappingOperation(usedIdentifier)
        currentlyUsed.append(taskIdentifier)
        result += " " + taskIdentifier

        amount = randrange(1, 2)
        j = 0
        for i in range(0, amount):
            rnd = randrange(0, len(self._taskIdentfier))
            taskIdentifier = self._taskIdentfier[rnd]
            while (
                taskIdentifier in usedRunningTogether
                or taskIdentifier in usedIdentifier
                or taskIdentifier in currentlyUsed
            ):
                j += 1
                rnd = randrange(0, len(self._taskIdentfier))
                taskIdentifier = self._taskIdentfier[rnd]
                if j >= 30:
                    return self._ProcessingOperation()
            currentlyUsed.append(taskIdentifier)
            result += ", " + taskIdentifier

        result += " ]"
        return (result, currentlyUsed)

    def _EquivalentOperation(self):
        result = ""

        rnd = randrange(0, 4)
        if rnd == 1:
            result = "NOT "

        rnd = randrange(len(self._mappingIdentifier))
        result += "EQUALS " + self._mappingIdentifier[rnd]
        return result
