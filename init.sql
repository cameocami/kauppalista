DELETE FROM departments;
DELETE FROM units;

INSERT into departments (name, display_name) VALUES
      ("fresh", "Hedelmät ja vihannekset"),
      ("baked", "Leivät ja leivonnaiset"),
      ("dairy", "Maitotuotteet"),
      ("meat_fish", "Liha, kala ja lihankorvikkeet"),
      ("ready_to_eat", "Valmisruoka"),
      ("pantry", "Kuivatuotteet"),
      ("drinks", "Juomat"),
      ("frozen", "Pakaste"),
      ("hygiene", "Hygieenia- ja kodinhoitotuotteet"),
      ("kids_pets", "Lapset ja eläimet"),
      ("other", "Muut");

INSERT into units (name, display_name) VALUES
      ("piece", "kpl"),
      ("kilogram", "kg"),
      ("liter", "l");