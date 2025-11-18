import logging
from datetime import datetime

from revomonauto.controllers.revo_controller import RevoAppController

# Set up logging
log_file = f"controller_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)

# Suppress PIL and adb_shell debug logs
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("adb_shell").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:

        controller = RevoAppController()

        logger.info("Opening Revomon app...")
        controller.open_revomon_app()
        while True:
            if controller.is_attacks_menu_scene():
                logger.info("Attacks menu scene detected.")
                break
            elif controller.is_battle_bag_scene():
                logger.info("Battle bag scene detected.")
                break
            elif controller.is_in_battle_scene():
                logger.info("In battle scene detected.")
                break
            elif controller.is_login_scene():
                logger.info("Login scene detected.")
                break
            else:
                logger.info("Unknown scene detected.")
                continue
    except Exception as e:
        logger.error(f"Controller Test: FAILED!!!\nError: {e}")