// ModItems
package ${package_name};

import static ${package_name}.${main_class_name}.MOD_ID;
import net.fabricmc.fabric.api.item.v1.FabricItemSettings;
import net.minecraft.item.FoodComponent;
import net.minecraft.item.Item;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import net.minecraft.util.Rarity;

public class ModItems {
    public static <T extends Item> T registryItem(T item, String id) {
        Registry.register(Registries.ITEM,
            new Identifier(MOD_ID, id),
            item
        );
        return item;
    }
    ${registers}
    public static void onRegistry() { }
}