

function showGraphQLData(){
    const query = `
        query {
            notebook(id:1) {
                id,
                name,
                model
            }
        }
    `;



    fetch("http://localhost:9992/gql/", {
        method: "POST",
        headers: {
        
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        body: JSON.stringify({
            query
        })
    }).then(response => {
        return response.json();
    }).then(data => {
        fetchedData(data)
    });

    // fetchedData = (apiData) => {
    //     console.log(apiData)
    // }

    fetchedData = (apiData) => {
        
        data = JSON.stringify(apiData);
        console.log(data)
        
       
        document.getElementById("demo").innerHTML = data;

    
    };

    

}

showGraphQLData()







// const GRAPHQL_URL = 'http://localhost:9992/gql/';

// const query = `
//     query {
//         notebook(id:1) {
//             id,
//             name,
//             model
//         }
//     }
// `;

// async function fetchGreeting() {
// const response = await fetch(GRAPHQL_URL, {
// method: 'POST',
// headers: {
// 'content-type': 'application/json',
// },
// body: JSON.stringify({
//     query
// }),
// });

// const { data } = await response.json();
// return data;
// }

// fetchGreeting().then(({ greeting }) => {
// const title = document.querySelector('h1');
// title.textContent = greeting;
// });



// from GraphQL wiki
// fetch('http://localhost:9992/gql/', {
// method: 'POST',
// headers: {
//     'Content-Type': 'application/json',
//     'Accept': 'application/json',
// },
// body: JSON.stringify({query: `{"query": "{notebook(id:1){name} }"}`})
// })
// .then(r => r.json())
// .then(data => console.log('data returned:', data));

