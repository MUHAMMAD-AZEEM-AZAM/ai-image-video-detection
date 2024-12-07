import React from 'react'
import styles from './Results.module.css';
const Table = ({
    humanPercentage,
aiPercentage
}) => {
  return (
    <table className={styles.table}>
    <thead>
        <tr>
            <th>Human</th>
            <th>AI</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                {humanPercentage}%
                <div className={styles.progressContainer}>
                    <div
                        
                    >
                        <progress value={humanPercentage} />
                    </div>
                </div>
            </td>
            <td>
                {aiPercentage}%
                <div className={styles.progressContainer}>
                    <div
                       
                    >
                     <progress value={aiPercentage} />   
                    </div>
                </div>
            </td>
        </tr>
    </tbody>
</table>
  )
}

export default Table