document.getElementById('filter-terminal').addEventListener('change', function() {
    // Lógica para filtrar la tabla por terminal
    console.log("Filtro por terminal: " + this.value);
});

document.getElementById('filter-proveedor').addEventListener('change', function() {
    // Lógica para filtrar la tabla por proveedor
    console.log("Filtro por proveedor: " + this.value);
});
