<template>
  <div id="app">
    <header>
      <h1>Projeto Django</h1>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  text-align: center;
}

header {
  background-color: #007bff;
  color: white;
  padding: 10px 0;
}

main {
  padding: 20px;
}
</style>