import React from 'react';
import { Link } from 'react-router-dom';
import HTML from '../../HTML/HTML';

interface ExperimentCollectionAboutProps {
    content: string;
    slug: string;
}

export const ExperimentCollectionAbout: React.FC<ExperimentCollectionAboutProps> = (props: ExperimentCollectionAboutProps) => {

    const { content, slug } = props;

    return (
        <div className="container">
            <Link className="btn btn-lg btn-outline-primary mt-3" to={`/collection/${slug}`}>
                <i className="fas fa-arrow-left mr-2"></i>
                Terug
            </Link>
            <div className="col-12 mt-3" role="contentinfo">
                <HTML body={content} innerClassName="prose text-left pb-3 text-white" />
            </div>
        </div>
    );
};

export default ExperimentCollectionAbout;