import React, { useState } from 'react';
import axios from 'axios';
import styles from './App.css'

const FaqSearch = () => {
  const [query, setQuery] = useState('');
  const [displayquery, setDisplayQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/query', { query });
      setResults(response.data);

      setDisplayQuery(query);
      setQuery('');

    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <div class='top'>
        <h1>similar item searcher</h1>
        <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Keywordを入力"
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      
      <div class='result'>
      {results.length > 0 && (
        <p><span>{displayquery}</span>に関連する特許情報</p>
      )}

        {results.map((item, index) => (
          <table align='center' key={index} cellSpacing='15' frame='box'>
            <tr>
              <th>法人番号</th>
              <td>{item[0]}</td>
            </tr>
            <tr>
              <th>法人名</th>
              <td>{item[1]}</td>
            </tr>
            <tr>
              <th>出願番号</th>
              <td>{item[2]}</td>
            </tr>
            <tr>
              <th>区分</th>
              <td>{item[3]}</td>
            </tr>
            <tr>
              <th>分類</th>
              <td>{item[4]}</td>
            </tr>
            <tr>
              <th>名称</th>
              <td>{item[5]}</td>
            </tr>
            <tr>
              <th>類似度</th>
              <td>{item[6]}</td>
            </tr>
          </table> 
        ))}
      </div>
      
    </div>
  );
};

export default FaqSearch;
