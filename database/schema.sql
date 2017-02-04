create table modules_history (
  id integer primary key autoincrement,
  target text not null,
  modules text not null
);