async function getCharacters() {
    let results = await fetch('http://localhost:9992/gql/?', {
      method: 'POST',
  
      headers: {
        "Content-Type": "application/json"
      },
  
      body: JSON.stringify({
        query: `query{
            notebook(id:1){
              name
            }
          }`
      })
    })
    let characters = await results.json();
    console.log(characters.data)
  }
  
  getCharacters()