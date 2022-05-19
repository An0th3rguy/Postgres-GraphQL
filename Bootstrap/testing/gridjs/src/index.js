

function DisplayTable(query, columns)

{


new gridjs.Grid({

  columns: columns,
  // data: [
  //   ["John", "john@example.com", "(353) 01 222 3333"],
  //   ["Mark", "mark@gmail.com", "(01) 22 888 4444"],
  //   ["Eoin", "eoin@gmail.com", "0097 22 654 00033"],
  //   ["Sarah", "sarahcdd@gmail.com", "+322 876 1233"],
  //   ["Afshin", "afshin@mail.com", "(353) 22 87 8356"]
  // ]

  server: {
    
    url: "http://localhost:9992/gql/",
    method: "POST",
    headers: {
        
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify({
            query
    }),

    // then: data => data.data.notebookAll.map(notebook => [notebook.name]), #musí vratit list, pokud vracím notebookAll vraci se mi list pokud vracim jen s konkretnim ID musim to sparsovat do listu/pole
    // then: data => data.data.notebookAll,

    //vraci pouze jedno pole => potřeba přetypovat na pole vložením do []
    then: (data => {
      match = [data.data.notebook]
      console.log(match)
      return match
    }),
    handle: (res) => {
        // no matching records found
        if (res.status === 404) return {data: []};
        if (res.ok) return res.json();
        
        throw Error('oh no :(');

    }
    
  },


}).render(document.getElementById("wrapper"));

}




const query = `
query {
    notebook(id:1) {
        id,
        name,
        model
        prices{
          price
        }
    }
}
`;

const columns = ["id","name","model","price"];

DisplayTable(query, columns)