import dobot_lib as dobot

def read_error_and_clear():
    error = dobot.get_error_id()
    if error is not None:
        print("Error detected, clearing error...\n")
        print(f"Error ID: {error}")
        dobot.clear_error()

def main():
    dobot.startup()
    dobot.power_on()
    dobot.enable_robot()
    dobot.set_speed_factor(50)
    dobot.set_collision_sensitivity(1)

    dobot.joint_movj(-350,-10,-135,50,90,320)

    read_error_and_clear()

    dobot.joint_movj(-350,-10,100,50,90,320)

    read_error_and_clear()

    dobot.clear_error()
    dobot.disable_robot()
    dobot.shutdown()

if __name__ == '__main__':
    main()
