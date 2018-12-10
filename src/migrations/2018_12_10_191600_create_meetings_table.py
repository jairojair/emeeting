from orator.migrations import Migration


class CreateMeetingsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("meetings") as table:
            table.increments("id")
            table.string("title")
            table.string("start")
            table.string("end")
            table.string("owner")
            table.timestamps()

            table.integer("room_id").unsigned()
            table.foreign("room_id").references("id").on("rooms").on_delete("cascade")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("meetings")
