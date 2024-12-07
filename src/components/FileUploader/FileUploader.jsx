// import { useState } from 'react';
// import './FileUploader.css';
// import { MdCloudUpload, MdDelete } from 'react-icons/md';
// import { AiFillFileImage } from 'react-icons/ai';

// function FileUploader({
//   file,
// setFile,
// fileName,
// setFileName,
// }) {
  

//   const handleFileChange = (event) => {
//     const file = event.target.files[0];
//     validateFile(file);
//   };

//   const handleDrop = (event) => {
//     event.preventDefault();
//     const file = event.dataTransfer.files[0];
//     validateFile(file);
//   };

//   const validateFile = (file) => {
//     if (file) {
//       const allowedTypes = ['image/', 'video/'];
//       if (allowedTypes.some(type => file.type.startsWith(type))) {
//         setFile(URL.createObjectURL(file));
//         setFileName(file.name);
//       } else {
//         alert("Only image and video files are allowed!");
//       }
//     }
//   };

//   return (
//     <main>
//       <form
//         onClick={() => document.querySelector(".input-field").click()}
//         onDragOver={(e) => e.preventDefault()} // Prevent default behavior for dragover
//         onDrop={handleDrop} // Handle drop event
//         className="file-uploader"
//       >
//         <input
//           type="file"
//           accept="image/*,video/*,video/mp4,video/avi,video/mpeg"
//           className="input-field"
//           hidden
//           onChange={handleFileChange}
//         />

//         {file ? (
//           <img src={file} height={250}  alt={fileName} />
//         ) : (
//           <>
//             <MdCloudUpload color="#1475cf" size={60} />
//             <p>Drag and drop files here or click to browse</p>
//           </>
//         )}
//       </form>

//       <section className="uploaded-row">
//         <AiFillFileImage color="#1475cf" />
//         <span className="upload-content">
//           {fileName} - 
//           <MdDelete
//             onClick={() => {
//               setFileName("No selected file");
//               setFile(null);
//             }}
//             size={20}
//           />
//         </span>
//       </section>
//     </main>
//   );
// }

// export default FileUploader;


import { useState } from 'react';
import './FileUploader.css';
import { MdCloudUpload, MdDelete } from 'react-icons/md';
import { AiFillFileImage } from 'react-icons/ai';

function FileUploader({
  file,
  setFile,
  fileName,
  setFileName,
}) {
  const [preview, setPreview] = useState(null); // For storing the preview URL

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    validateFile(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    validateFile(file);
  };

  const validateFile = (file) => {
    if (file) {
      const allowedTypes = ['image/', 'video/'];
      if (allowedTypes.some(type => file.type.startsWith(type))) {
        setFile(file); // Store the actual File object
        setFileName(file.name); // Set file name
        setPreview(URL.createObjectURL(file)); // Generate preview URL
      } else {
        alert("Only image and video files are allowed!");
      }
    }
  };

  const handleFileDelete = () => {
    setFileName("No selected file");
    setFile(null);
    setPreview(null); // Clear the preview
  };

  return (
    <main>
      <form
        onClick={() => document.querySelector(".input-field").click()}
        onDragOver={(e) => e.preventDefault()} // Prevent default behavior for dragover
        onDrop={handleDrop} // Handle drop event
        className="file-uploader"
      >
        <input
          type="file"
          accept="image/*,video/*,video/mp4,video/avi,video/mpeg"
          className="input-field"
          hidden
          onChange={handleFileChange}
        />

        {preview ? (
          <img src={preview} height={250} alt={fileName} />
        ) : (
          <>
            <MdCloudUpload color="#1475cf" size={60} />
            <p>Drag and drop files here or click to browse</p>
          </>
        )}
      </form>

      {file && (
        <section className="uploaded-row">
          <AiFillFileImage color="#1475cf" />
          <span className="upload-content">
            {fileName} - 
            <MdDelete
              onClick={handleFileDelete}
              size={20}
            />
          </span>
        </section>
      )}
    </main>
  );
}

export default FileUploader;
