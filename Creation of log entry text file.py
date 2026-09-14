
 def create_logbook():
     with open("accessLogs.txt","w") as file:
         file.write("------------------------------------------------------------------------------\n")
         file.write(f"{'ACCESS LOGS':>45}")
         file.write("\n------------------------------------------------------------------------------\n")
         file.write(f"{'LOG NO.'}{'BINARY CODE':>14}{'USER TYPE':>15}{'RESULT':>15}{'ACCESS COUNT':>15}{'TIME':>8}")
         file.write("\n------------------------------------------------------------------------------")
  
create_logbook()

