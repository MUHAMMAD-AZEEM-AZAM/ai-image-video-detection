import React from 'react';
import styles from './Results.module.css';
import Table from './Table';
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
const Results = ({ response }) => {
    console.log("The response is: ", response)
    return (
        <div style={{height:'64vh'}}>

            {response?.AIvsHuman?.status === 'ai' ? (<div className={`${styles.guage} ${styles.card}`}>
                <Gauge width={140} height={140} value={Math.floor(response?.AIvsHuman?.score * 10000) / 100} title='Ai'
                 sx={() => ({
                    [`& .${gaugeClasses.valueArc}`]: {
                      fill: '#dc2f02',
                    },
                    
                  })}
                />
                <h4>AI Genrated</h4>

            </div>) : (<div className={`${styles.guage} ${styles.card}`}>
                <Gauge width={140} height={140} value={Math.floor(response?.AIvsHuman?.score * 10000) / 100} title='Human' />
                <h4>Made By Human</h4>
            </div>)}
            {/* <Table
                humanPercentage={humanPercentage}
                aiPercentage={aiPercentage}
      </div>      /> */}
            <div style={{display:'flex',gap:'10px'}}>
                <div className={`${styles.guage} ${styles.card}`}>
                    <h4>NSFW Status</h4>
                    <Gauge width={140} height={140} value={response?.nsfw_status?.score * 100} title='nsfw' 
                     sx={(theme) => ({
                        [`& .${gaugeClasses.valueArc}`]: {
                          fill: `${response?.nsfw_status?.status ? '#dc2f02' : '#1976d2'}`,
                        },
                        
                      })}
                    />
                    <div>
                    <p>{response?.nsfw_status?.reason}</p>
                    </div>
                </div>
                <div className={`${styles.guage} ${styles.card}`}>
                    <h4>Quality</h4>
                    <Gauge width={140} height={140} value={response?.quality_results?.score * 100} title='quality' 
                     sx={(theme) => ({
                        [`& .${gaugeClasses.valueArc}`]: {
                          fill: `${response?.quality_results?.status=="Low" ? '#dc2f02' : '#1976d2'}`,
                        },
                        
                      })}
                    />
                    <div>
                    <p>{response?.quality_results?.status}</p>
                    </div>
                </div>
            </div>
            {/* <h4>NSFW Status</h4>
            <div className={styles.detail} style={{ backgroundColor: `${!response?.nsfw_status?.status ? '#7bf266' : '#ffb3c1'}` }}>
                <p>{response?.nsfw_status?.reason}</p>
            </div>
            <h4>Image Quality</h4>
            <div className={styles.detail} style={{ backgroundColor: `${response?.quality_results?.status == "Low" ? '#ffb3c1' : '#7bf266'}` }}>
                <p>{response?.quality_results?.status} Quality</p>
            </div> */}
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
