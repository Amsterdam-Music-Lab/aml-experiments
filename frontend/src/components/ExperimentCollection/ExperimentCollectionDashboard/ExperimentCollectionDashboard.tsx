import React from "react";
import { Link } from "react-router-dom";

import { API_ROOT } from "@/config";
import ExperimentCollection from "@/types/ExperimentCollection";
import AppBar from "@/components/AppBar/AppBar";
import Header from "@/components/Header/Header";


interface ExperimentCollectionDashboardProps {
    experimentCollection: ExperimentCollection;
    participantIdUrl: string | null;
}

export const ExperimentCollectionDashboard: React.FC<ExperimentCollectionDashboardProps> = ({ experimentCollection, participantIdUrl, totalScore }) => {
    
    const dashboard = experimentCollection.dashboard;
    const nextExperimentSlug = experimentCollection.nextExperiment?.slug;   
    
    const headerProps = experimentCollection.theme?.header? {
        nextExperimentSlug,        
        collectionSlug: experimentCollection.slug,
        ...experimentCollection.theme.header,
        totalScore: totalScore
        
    } : undefined;
    
    const getExperimentHref = (slug: string) => `/${slug}${participantIdUrl ? `?participant_id=${participantIdUrl}` : ""}`;

    return (
        <>
        <AppBar title={experimentCollection.name} logoClickConfirm="placeholder text" />
        {headerProps && (
            <Header { ...headerProps }></Header>
        )}
            {/* Experiments */}
            <div role="menu" className="dashboard">
                <ul>
                    {dashboard.map((exp) => (
                        <li key={exp.slug}>
                            <Link to={getExperimentHref(exp.slug)} role="menuitem">
                                <ImageOrPlaceholder imagePath={exp.image} alt={exp.description} />
                                <h3>{exp.name}</h3>
                                <div className="status-bar">
                                    <span title={`Started ${exp.started_session_count} times`} role="status" className="counter">{exp.started_session_count}</span>
                                    <span title={`Started ${exp.finished_session_count} times`} role="status" className="counter">{exp.finished_session_count}</span>
                                </div>
                            </Link>
                        </li>
                    ))}
                    {dashboard.length === 0 && <p>No experiments found</p>}
                </ul>
            </div>
        </>
    );
}

const ImageOrPlaceholder = ({ imagePath, alt }: { imagePath: string, alt: string }) => {
    const imgSrc = imagePath ? `${API_ROOT}/${imagePath}` : null;

    return imgSrc ? <img src={imgSrc} alt={alt} /> : <div className="placeholder" />;
}

export default ExperimentCollectionDashboard;
