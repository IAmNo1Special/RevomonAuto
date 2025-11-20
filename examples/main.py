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
        logging.info("Initializing BluePyllController...")
        controller = BluePyllController()
        logging.info("BluePyllController initialized successfully.")

        logging.info("Initializing RevomonApp...")
        revomon_app = RevomonApp(controller)
        logging.info("RevomonApp initialized successfully.")

        logging.info("Opening BlueStacks...")
        controller.bluestacks.open()
        logging.info("BlueStacks opened successfully.")

        logging.info("Opening Revomon App...")
        revomon_app.open_revomon_app()
        logging.info("Revomon App opened successfully.")

        logging.info("Starting Game...")
        revomon_app.start_game()
        logging.info("Game started successfully.")

        logging.info("Logging in...")
        revomon_app.login()
        logging.info("Login successful.")

        logging.info("Opening Main Menu...")
        revomon_app.open_main_menu()
        logging.info("Main menu opened successfully.")

        logging.info("Closing Main Menu...")
        revomon_app.close_main_menu()
        logging.info("Main menu closed successfully.")

        logging.info("Entering PVP Queue...")
        revomon_app.enter_pvp_queue()
        logging.info("PVP Queue entered successfully.")

        logging.info("Exiting PVP Queue...")
        revomon_app.exit_pvp_queue()
        logging.info("PVP Queue exited successfully.")

        logging.info("Opening wardrobe...")
        revomon_app.open_wardrobe()
        logging.info("Wardrobe opened successfully.")

        logging.info("Closing wardrobe")
        revomon_app.close_wardrobe()
        logging.info("Wardrobe closed successfully.")

        logging.info("Opening menu bag...")
        revomon_app.open_menu_bag()
        logging.info("Menu bag opened successfully.")

        logging.info("Closing menu bag...")
        revomon_app.close_menu_bag()
        logging.info("Menu bag closed successfully.")

        logging.info("Opening friends list...")
        revomon_app.open_friends_list()
        logging.info("Friends list opened successfully.")

        logging.info("Closing friends list...")
        revomon_app.close_friends_list()
        logging.info("Friends list closed successfully.")

        logging.info("Opening settings...")
        revomon_app.open_settings()
        logging.info("Settings opened successfully.")

        logging.info("Closing settings...")
        revomon_app.close_settings()
        logging.info("Settings closed successfully.")

        logging.info("Opening revodex...")
        revomon_app.open_revodex()
        logging.info("Revodex opened successfully.")

        logging.info("Closing revodex...")
        revomon_app.close_revodex()
        logging.info("Revodex closed successfully.")

        logging.info("Opening market...")
        revomon_app.open_market()
        logging.info("Market opened successfully.")

        logging.info("Closing market...")
        revomon_app.close_market()
        logging.info("Market closed successfully.")

        logging.info("Opening discussion...")
        revomon_app.open_discussion()
        logging.info("Discussion opened successfully.")

        logging.info("Closing discussion...")
        revomon_app.close_discussion()
        logging.info("Discussion closed successfully.")

        logging.info("Opening clan...")
        revomon_app.open_clan()
        logging.info("Clan opened successfully.")

        logging.info("Closing clan...")
        revomon_app.close_clan()
        logging.info("Clan closed successfully.")

        input("Press Enter once you are in a battle to continue...")
        while True:
            if revomon_app.is_in_battle_scene():
                logging.info("Opening attacks menu...")
                revomon_app.open_attacks_menu()
                logging.info("Attacks menu opened successfully.")

                logging.info("choosing random attack...")
                revomon_app.choose_move()
                logging.info("Random attack chosen successfully.")

        logging.info("Closing Revomon App...")
        revomon_app.close_revomon_app()
        logging.info("Revomon App closed successfully.")

        logging.info("Closing BlueStacks...")
        controller.bluestacks.kill_bluestacks()
        logging.info("BlueStacks closed successfully.")

    except Exception:
        logging.exception("An error occurred during execution")
