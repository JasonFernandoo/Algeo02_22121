var apiUrl = "http://127.0.0.1:5000/calculate/";

async function productTable() {
    const data = await fetch();
    const res = await data.json();
    console.log(res);
}
productTable()