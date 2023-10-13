import React, { useState } from 'react';

function App() {
  const [tokenId, setTokenId] = useState('');
  const [rarityResults, setRarityResults] = useState('');
  const [selectedTokenData, setSelectedTokenData] = useState(null);

  const fetchData = () => {
    // Fetch JSON data using a relative path
    fetch('./data.json')
      .then(response => response.json())
      .then(jsonData => {
        if (jsonData[tokenId] && jsonData[tokenId].data) {
          setSelectedTokenData(jsonData[tokenId]);
        } else {
          setSelectedTokenData(null);
        }
      })
      .catch(error => {
        console.error('Error fetching JSON data:', error);
        setSelectedTokenData(null); // Clear the selected data on error
      });
  };

  const checkRarity = () => {
    if (selectedTokenData) {
      const traits = selectedTokenData.data.attributes;
      const rarity = {
        background: {},
        Character: {},
        Eyes: {},
        Mouth: {},
      };

      traits.forEach((trait) => {
        rarity[trait.trait_type][trait.value] = (rarity[trait.trait_type][trait.value] || 0) + 1;
      });

      const rarityText = `
        Background Rarity: ${Object.keys(rarity.background).length} unique traits
        Character Rarity: ${Object.keys(rarity.Character).length} unique traits
        Eyes Rarity: ${Object.keys(rarity.Eyes).length} unique traits
        Mouth Rarity: ${Object.keys(rarity.Mouth).length} unique traits
      `;

      setRarityResults(rarityText);
    } else {
      setRarityResults('Token ID not found in the JSON data. Fetch the data first.');
    }
  };

  return (
    <div className="App">
      <h1>NFT Rarity Checker</h1>
      <label htmlFor="tokenId">Enter Token ID:</label>
      <input
        type="text"
        id="tokenId"
        placeholder="Enter Token ID"
        value={tokenId}
        onChange={(e) => setTokenId(e.target.value)}
      />
      <button onClick={fetchData}>Fetch Data</button>
      {selectedTokenData && (
        <div>
          <h2>Data for Token ID {tokenId}:</h2>
          <pre>{JSON.stringify(selectedTokenData, null, 2)}</pre>
        </div>
      )}
      <button onClick={checkRarity}>Check Rarity</button>
      <div id="rarityResults">{rarityResults}</div>
    </div>
  );
}

export default App;