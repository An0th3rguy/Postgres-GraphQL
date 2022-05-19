async function getCharacters() {
    let results = await fetch('https://rickandmortyapi.com/graphql', {
      method: 'POST',
  
      headers: {
        "Content-Type": "application/json"
      },
  
      body: JSON.stringify({
        query: `{
          characters {
            results {
              name
            }
          }
        }`
      })
    })
    let characters = await results.json();
    console.log(characters.data)
  }
  
  getCharacters()