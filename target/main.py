import formatter
import sandbox

#max local distance between targets to state they are the same (m)
# maxDist = 25

#input mission files
nameOne = "test1"
# nameTwo = "test2"

# name of output file
# outputName = "Comparison"

# build target list from input COIN PMD Reports
missionOne = formatter.coinTargetFormatter( nameOne)  
# missionTwo = formatter.coinTargetFormatter( nameTwo)

# build output comparison from target lists
# tformatter.compareOutput( missionOne, missionTwo, maxDist, outputName)

# test out training range status formatter
nameThree = 'test3'

fields = sandbox.rangeTargetFormatter( nameThree)
# tformatter.printTargets( fields)
# sandbox.vipOutput(fields, "temp")