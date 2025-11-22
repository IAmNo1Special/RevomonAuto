import logging
import sys
import threading

from bluepyll import BluePyllController

from revomonauto.models.revomon_app import RevomonApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

if __name__ == "__main__":
    try:

        logging.info("Initializing RevomonApp...")
        revomon_app = RevomonApp()
        logging.info("RevomonApp initialized successfully.")

        logging.info("Initializing BluePyllController...")
        controller = BluePyllController(apps=[revomon_app])
        logging.info("BluePyllController initialized successfully.")

        logging.info("Opening BlueStacks...")
        controller.bluestacks.open()
        logging.info("BlueStacks opened successfully.")

        logging.info("Opening Revomon App...")
        controller.revomon.open_revomon_app()
        logging.info("Revomon App opened successfully.")

        logging.info("Starting Game...")
        controller.revomon.start_game()
        logging.info("Game started successfully.")

        logging.info("Logging in...")
        controller.revomon.login()
        logging.info("Login successful.")

        logging.info("Opening clan...")
        # TODO: When the player isn't in a clan then this is broken to act as if they are
        # Since there is no screen check to see if the player is in a clan, this triggers regardless of the player's clan status
        # controller.revomon.open_clan()
        logging.info("Clan opened successfully.")

        logging.info("Closing clan...")
        # TODO: Since there is no screen check to see if the player is in a clan
        # TODO: When the player isn't in a clan then this closes the main menu(mistaking it for the clan screen)
        # and gets stuck in a loop waiting to confirm it's now on the main menu
        # controller.revomon.close_clan()
        logging.info("Clan closed successfully.")

        input("Press Enter once you are in a battle to continue...")

        # Setup cross-platform Enter key detection
        stop_battle = threading.Event()

        def wait_for_enter():
            input("Press Enter at any time to stop auto-battle...\n")
            stop_battle.set()

        # Start the input listener thread
        input_thread = threading.Thread(target=wait_for_enter, daemon=True)
        input_thread.start()

        logging.info("Auto-battle started. Press Enter at any time to stop...")
        while True:
            # Check if Enter key was pressed
            if stop_battle.is_set():
                logging.info("Enter pressed - exiting auto-battle loop...")
                break

            if controller.revomon.is_on_battle_screen():
                logging.info("Battle detected. Deciding action...")
                chosen_action = controller.revomon.choose_move()
                logging.info(f"Decided Action: {chosen_action}")
                #logging.info(f"Action Message: {chosen_action.action_message}")

        logging.info("Closing Revomon App...")
        controller.revomon.close_revomon_app()
        logging.info("Revomon App closed successfully.")

        logging.info("Closing BlueStacks...")
        controller.bluestacks.kill_bluestacks()
        logging.info("BlueStacks closed successfully.")

    except Exception:
        logging.exception("An error occurred during execution")
