import logging
import sys

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

        logging.info("Opening Main Menu...")
        controller.revomon.open_main_menu()
        logging.info("Main menu opened successfully.")

        logging.info("Closing Main Menu...")
        controller.revomon.close_main_menu()
        logging.info("Main menu closed successfully.")

        logging.info("Entering PVP Queue...")
        controller.revomon.enter_pvp_queue()
        logging.info("PVP Queue entered successfully.")

        logging.info("Exiting PVP Queue...")
        controller.revomon.exit_pvp_queue()
        logging.info("PVP Queue exited successfully.")

        logging.info("Opening wardrobe...")
        controller.revomon.open_wardrobe()
        logging.info("Wardrobe opened successfully.")

        logging.info("Closing wardrobe")
        controller.revomon.close_wardrobe()
        logging.info("Wardrobe closed successfully.")

        logging.info("Opening menu bag...")
        controller.revomon.open_menu_bag()
        logging.info("Menu bag opened successfully.")

        logging.info("Closing menu bag...")
        controller.revomon.close_menu_bag()
        logging.info("Menu bag closed successfully.")

        logging.info("Opening friends list...")
        controller.revomon.open_friends_list()
        logging.info("Friends list opened successfully.")

        logging.info("Closing friends list...")
        controller.revomon.close_friends_list()
        logging.info("Friends list closed successfully.")

        logging.info("Opening settings...")
        controller.revomon.open_settings()
        logging.info("Settings opened successfully.")

        logging.info("Closing settings...")
        controller.revomon.close_settings()
        logging.info("Settings closed successfully.")

        logging.info("Opening revodex...")
        controller.revomon.open_revodex()
        logging.info("Revodex opened successfully.")

        logging.info("Closing revodex...")
        controller.revomon.close_revodex()
        logging.info("Revodex closed successfully.")

        logging.info("Opening market...")
        controller.revomon.open_market()
        logging.info("Market opened successfully.")

        logging.info("Closing market...")
        controller.revomon.close_market()
        logging.info("Market closed successfully.")

        logging.info("Opening discussion...")
        controller.revomon.open_discussion()
        logging.info("Discussion opened successfully.")

        logging.info("Closing discussion...")
        controller.revomon.close_discussion()
        logging.info("Discussion closed successfully.")

        logging.info("Opening clan...")
        controller.revomon.open_clan()
        logging.info("Clan opened successfully.")

        logging.info("Closing clan...")
        controller.revomon.close_clan()
        logging.info("Clan closed successfully.")

        input("Press Enter once you are in a battle to continue...")
        while True:
            if controller.revomon.is_in_battle_scene():
                logging.info("Opening attacks menu...")
                controller.revomon.open_attacks_menu()
                logging.info("Attacks menu opened successfully.")

                logging.info("choosing random attack...")
                controller.revomon.choose_move()
                logging.info("Random attack chosen successfully.")

        logging.info("Closing Revomon App...")
        controller.revomon.close_revomon_app()
        logging.info("Revomon App closed successfully.")

        logging.info("Closing BlueStacks...")
        controller.bluestacks.kill_bluestacks()
        logging.info("BlueStacks closed successfully.")

    except Exception:
        logging.exception("An error occurred during execution")
