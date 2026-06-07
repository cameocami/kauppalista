DELETE FROM departments;
DELETE FROM units;

INSERT into departments (name) VALUES
      ('uncategorized'),
      ('fresh'),
      ('baked'),
      ('dairy'),
      ('meat_fish'),
      ('ready_to_eat'),
      ('pantry'),
      ('drinks'),
      ('frozen'),
      ('hygiene'),
      ('kids_pets');

INSERT into units (name) VALUES
      ('piece'),
      ('kilogram'),
      ('liter');