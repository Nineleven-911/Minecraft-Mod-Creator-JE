package ${package_name};

import ${package_name}.*;
import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ${main_class_name} implements ModInitializer {
    public static final String MOD_ID = "${mod_id}";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        LOGGER.info("--------------------");
        LOGGER.info("This mod made by Python auto mod generator Minecraft-Mod-Creator, MMC. GitHub: https://github.com/Nineleven-911/Minecraft-Mod-Creator-JE");
        LOGGER.info("${main_class_name} mod start.");
        LOGGER.info("Event activated: \"onInitialize\".");

        // Events
        ${activating_functions}

        LOGGER.info("onInitialize execution complete.\n");
    }
}
