

function showGraphQLData(){
    const query = `
    mutation{
        createVendor(
          vendor: {
            name: "Alzaaa"
            address: "Klementovice 58468"
            telephone: "+420 727 812 109"
          }
        ) {
          ok
        }
      }`;



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
        console.log(JSON.stringify(data))
        
    });

    

}

showGraphQLData()
