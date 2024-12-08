import React, { useState } from 'react';
import FileUploader from '../../components/FileUploader/FileUploader';
import './Home.css';
import useDataPosting from '../../hook/useDataPosting';
import CustomButton from '../../components/CustomButton';
import Results from '../../components/Results/Results';

const Home = () => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("No selected file");
  const { response, loading, error, postData, statusCode } = useDataPosting('predict'); // Replace with your URL

  const handleProcess =async () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
    await  postData(formData);
    } else {
      alert("No file selected!");
    }
  };

  return (
<div className='main-row'>
<div className='home-container'>
      <FileUploader
        file={file}
        setFile={setFile}
        fileName={fileName}
        setFileName={setFileName}
      />
      <div style={{display:'flex',flexDirection:'column',gap:'10px'}}>
        <div style={{display:'flex', justifyContent:'center'}}>
      <CustomButton onClick={handleProcess} loading={loading} disabled={!file}>
        Process
      </CustomButton>
        </div>
      {error && <p className='error'>{error.message}</p>}
      {response && <p className='success'>File uploaded successfully!</p>}
      </div>
    </div>
{statusCode===200 &&<Results response={response}/>}
</div>
  
  );
};

export default Home;