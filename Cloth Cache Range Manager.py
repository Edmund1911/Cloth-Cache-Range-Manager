bl_info = {
    "name": "Cloth Cache Range Manager",
    "author": "Edmund1911, with ChatGPT",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "3D View > Sidebar > Cloth",
    "description": "Manage and sync Cloth simulation cache frame ranges",
    "category": "Physics",
}


import bpy


# =========================================================
# Sync All Cloth
# =========================================================

class CLOTHMANAGER_OT_sync_all(bpy.types.Operator):
    bl_idname = "cloth_manager.sync_all"
    bl_label = "Sync All Cloth"
    bl_description = "Sync all Cloth cache ranges to the Scene frame range"

    def execute(self, context):

        scene = context.scene
        count = 0

        for obj in scene.objects:

            for mod in obj.modifiers:

                if mod.type == 'CLOTH':

                    cache = mod.point_cache

                    cache.frame_start = scene.frame_start
                    cache.frame_end = scene.frame_end

                    count += 1

                    # 一個物件只處理第一個 Cloth Modifier
                    break

        if count == 0:

            self.report(
                {'WARNING'},
                "No Cloth objects found"
            )

        else:

            self.report(
                {'INFO'},
                f"Updated {count} Cloth objects"
            )

        return {'FINISHED'}


# =========================================================
# Sync Selected Cloth
# =========================================================

class CLOTHMANAGER_OT_sync_selected(bpy.types.Operator):
    bl_idname = "cloth_manager.sync_selected"
    bl_label = "Sync Selected Cloth"
    bl_description = (
        "Sync selected Cloth cache ranges "
        "to the Scene frame range"
    )

    def execute(self, context):

        scene = context.scene
        count = 0

        for obj in context.selected_objects:

            for mod in obj.modifiers:

                if mod.type == 'CLOTH':

                    cache = mod.point_cache

                    cache.frame_start = scene.frame_start
                    cache.frame_end = scene.frame_end

                    count += 1

                    break

        if count == 0:

            self.report(
                {'WARNING'},
                "No selected Cloth objects found"
            )

        else:

            self.report(
                {'INFO'},
                f"Updated {count} selected Cloth objects"
            )

        return {'FINISHED'}


# =========================================================
# Select One Mismatched Object
# =========================================================

class CLOTHMANAGER_OT_select_object(bpy.types.Operator):
    bl_idname = "cloth_manager.select_object"
    bl_label = "Select Cloth Object"
    bl_description = "Select this Cloth object"

    object_name: bpy.props.StringProperty(
        name="Object Name"
    )

    def execute(self, context):

        obj = bpy.data.objects.get(self.object_name)

        if obj is None:

            self.report(
                {'WARNING'},
                f"Object not found: {self.object_name}"
            )

            return {'CANCELLED'}

        # 清除目前選取
        bpy.ops.object.select_all(
            action='DESELECT'
        )

        # 選取目標物件
        obj.select_set(True)

        # 設為 Active Object
        context.view_layer.objects.active = obj

        self.report(
            {'INFO'},
            f"Selected: {obj.name}"
        )

        return {'FINISHED'}


# =========================================================
# Select All Mismatched Cloth
# =========================================================

class CLOTHMANAGER_OT_select_all_mismatched(
    bpy.types.Operator
):
    bl_idname = "cloth_manager.select_all_mismatched"
    bl_label = "Select All Mismatched"
    bl_description = (
        "Select all Cloth objects whose cache ranges "
        "do not match the Scene frame range"
    )

    def execute(self, context):

        scene = context.scene

        bpy.ops.object.select_all(
            action='DESELECT'
        )

        count = 0
        first_obj = None

        for obj in scene.objects:

            for mod in obj.modifiers:

                if mod.type == 'CLOTH':

                    cache = mod.point_cache

                    if (
                        cache.frame_start != scene.frame_start
                        or
                        cache.frame_end != scene.frame_end
                    ):

                        obj.select_set(True)

                        if first_obj is None:
                            first_obj = obj

                        count += 1

                    # 一個物件只檢查第一個 Cloth Modifier
                    break

        # 把第一個 mismatch 設為 Active Object
        if first_obj is not None:

            context.view_layer.objects.active = first_obj

        if count == 0:

            self.report(
                {'INFO'},
                "No mismatched Cloth objects found"
            )

        else:

            self.report(
                {'INFO'},
                f"Selected {count} mismatched Cloth objects"
            )

        return {'FINISHED'}


# =========================================================
# Main Panel
# =========================================================

class CLOTHMANAGER_PT_main_panel(bpy.types.Panel):

    bl_label = "Cloth Cache Range Manager"
    bl_idname = "CLOTHMANAGER_PT_main_panel"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cloth"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        # -------------------------------------------------
        # Scene Range
        # -------------------------------------------------

        layout.label(
            text="Scene Range"
        )

        layout.prop(
            scene,
            "frame_start",
            text="Start"
        )

        layout.prop(
            scene,
            "frame_end",
            text="End"
        )

        # -------------------------------------------------
        # Scan Cloth Objects
        # -------------------------------------------------

        cloth_count = 0
        mismatched_objects = []

        for obj in scene.objects:

            for mod in obj.modifiers:

                if mod.type == 'CLOTH':

                    cloth_count += 1

                    cache = mod.point_cache

                    if (
                        cache.frame_start != scene.frame_start
                        or
                        cache.frame_end != scene.frame_end
                    ):

                        mismatched_objects.append(obj)

                    # 一個 Object 只計算一次
                    break

        # -------------------------------------------------
        # Cloth Information
        # -------------------------------------------------

        layout.separator()

        layout.label(
            text=f"Found Cloth: {cloth_count}"
        )

        # -------------------------------------------------
        # Mismatch Information
        # -------------------------------------------------

        if len(mismatched_objects) == 0:

            layout.label(
                text="All Cloth ranges match Scene",
                icon='CHECKMARK'
            )

        else:

            layout.label(
                text=f"Mismatched: {len(mismatched_objects)}",
                icon='ERROR'
            )

            # Select All
            layout.operator(
                "cloth_manager.select_all_mismatched",
                text="Select All Mismatched",
                icon='RESTRICT_SELECT_OFF'
            )

            # Mismatch List
            box = layout.box()

            for obj in mismatched_objects:

                row = box.row(
                    align=True
                )

                row.label(
                    text=obj.name,
                    icon='OBJECT_DATA'
                )

                op = row.operator(
                    "cloth_manager.select_object",
                    text="",
                    icon='RESTRICT_SELECT_OFF'
                )

                op.object_name = obj.name

        # -------------------------------------------------
        # Sync Operations
        # -------------------------------------------------

        layout.separator()

        layout.operator(
            "cloth_manager.sync_selected",
            text="Sync Selected Cloth",
            icon='RESTRICT_SELECT_OFF'
        )

        layout.operator(
            "cloth_manager.sync_all",
            text="Sync All Cloth",
            icon='FILE_REFRESH'
        )


# =========================================================
# Classes
# =========================================================

classes = (
    CLOTHMANAGER_OT_sync_all,
    CLOTHMANAGER_OT_sync_selected,
    CLOTHMANAGER_OT_select_object,
    CLOTHMANAGER_OT_select_all_mismatched,
    CLOTHMANAGER_PT_main_panel,
)


# =========================================================
# Register
# =========================================================

def register():

    for cls in classes:

        bpy.utils.register_class(cls)


# =========================================================
# Unregister
# =========================================================

def unregister():

    for cls in reversed(classes):

        bpy.utils.unregister_class(cls)


# =========================================================
# Development / Text Editor Test
# =========================================================

if __name__ == "__main__":

    register()