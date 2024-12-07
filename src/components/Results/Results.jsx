import React from 'react';
import styles from './Results.module.css';
import Table from './Table';
import { Gauge } from '@mui/x-charts/Gauge';
const Results = ({ response }) => {
    const humanPercentage = 50;
    const aiPercentage = 50;
    console.log("The response is: ", response)
    return (
        <div>

            {response?.AIvsHuman?.status === 'ai' ? (<div className={styles.guage}>
                <Gauge width={180} height={180} value={response?.AIvsHuman?.score * 100} title='Ai' />

                <h4>AI Genrated</h4>

            </div>) : (<div className={styles.guage}>
                <Gauge width={180} height={180} value={response?.AIvsHuman?.score * 100} title='Human' />
                <h4>Made By Human</h4>
            </div>)}
            {/* <Table
                humanPercentage={humanPercentage}
                aiPercentage={aiPercentage}
            /> */}
            <h4>NSFW Status</h4>
            <div className={styles.detail} style={{backgroundColor:`${response?.nsfw_status?.status=='Safe'?'#7bf266':'#ffb3c1'}`}}>
                <p>{response?.nsfw_status?.status}</p>
                <p>{response?.nsfw_status?.reason}</p>
            </div>
            <h4>Image Quality</h4>
            <div className={styles.detail} style={{backgroundColor:`${response?.image_quality_results?.is_low_quality?'#ffb3c1':'#7bf266'}`}}>
                <p>{response?.image_quality_results?.is_low_quality?'Bad Quality':'Good Quality'}</p>
                <p>{Math.round(response?.image_quality_results?.results * 100)}% Quality</p>
            </div>
        </div>
    );
}

export default Results;

// {
//   "AIvsHuman": {
//     "score": 0.9996103644371033,
//     "status": "ai"
//   },
//   "image_quality_results": {
//     "is_low_quality": false,
//     "results": 0.7611987080090779
//   },
//   "nsfw_status": {
//     "probability": false,
//     "reason": "Normal",
//     "status": "Safe"
//   }
// }
