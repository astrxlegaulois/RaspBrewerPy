mon_step1=Step("monStep",TRANSITION,10)
mon_step2=Step("monStep2",LEVEL,60,67)
mon_step3=Step("monStep3",TRANSITION,10)
mon_step4=Step("monStep4",LEVEL,1,90)
mon_step1.print_self()
mon_step2.print_self()
mon_step3.print_self()
mon_step4.print_self()

mon_step1.interpolation(0, datetime.datetime.now(), 50, datetime.datetime.now()+ datetime.timedelta(minutes=5, seconds=0))

ma_receipe=Receipe("Ma première recette")
ma_receipe.add_step(mon_step1)
ma_receipe.add_step(mon_step2)
ma_receipe.add_step(mon_step3)
ma_receipe.add_step(mon_step4)

ma_receipe.print_self()

ma_receipe.start(20)
ma_receipe.print_self()

ma_receipe.get_current_temperature_instruction()
ma_receipe.update_step()
ma_receipe.print_self()

ma_receipe.user_force_next_step()
ma_receipe.print_self()
ma_receipe.get_current_temperature_instruction()

ma_receipe.user_force_next_step()
ma_receipe.print_self()
ma_receipe.get_current_temperature_instruction()

ma_receipe.user_force_next_step()
ma_receipe.print_self()
ma_receipe.get_current_temperature_instruction()

ma_receipe.user_force_next_step()
ma_receipe.print_self()
ma_receipe.get_current_temperature_instruction()
