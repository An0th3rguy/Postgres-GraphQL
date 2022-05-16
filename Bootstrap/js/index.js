

function DisplayTable(query, columns, id, type)

{


new gridjs.Grid({

  search: {
    enabled: true
  },

  sort: true,

  pagination: {
    enabled: true,
    limit: 6,
    summary: false
  },

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

    // then: data => data.data.vendorAll, //musí vratit list, pokud vracím notebookAll vraci se mi list pokud vracim jen s konkretnim ID musim to sparsovat do listu/pole
    // then: data => data.data.notebookAll,

    // vraci pouze jedno pole => potřeba přetypovat na pole vložením do []
    then: (data => {
      
      if(type=="ShowAllVendors")
        return data.data.vendorAll
      else if(type == "ShowAllNotebooks")
        return data.data.notebookAll
      // match = [data.data.notebook]
      // console.log(match)
      // return match
    }),

    handle: (res) => {
        // no matching records found
        if (res.status === 404) return {data: []};
        if (res.ok) return res.json();
        
        throw Error('oh no :(');

    },
    
  },


}).render(document.getElementById(id));

}

document.getElementById("wrapper").innerHTML = DisplayTable(`query{notebookAll{id,name,model }}`, ["id","name","model"], "wrapper","ShowAllNotebooks")
document.getElementById("wrapper").innerHTML = DisplayTable(`query{vendorAll{id,name,address }}`, ["id","name","address"], "wrapper2", "ShowAllVendors")






