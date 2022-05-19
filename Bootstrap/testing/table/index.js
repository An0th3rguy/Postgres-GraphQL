

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
      console.log(apiData)
      
     
      document.getElementById("demo").innerHTML = data;

      new gridjs.Grid({
        columns: ["id", "Email", "Phone Number","sadasd"],
        data: [
          apiData
        ]
      }).render(document.getElementById("wrapper"));
  
  };

  

}

showGraphQLData()








