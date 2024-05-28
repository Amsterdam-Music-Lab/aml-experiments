export interface Header {
    nextExperimentButtonText: string;
    aboutButtonText: string;
    showScore: boolean;
    totalScore: BigInteger;
};

export default interface Theme {
    backgroundUrl: string;
    bodyFontUrl: string;
    description: string;
    headingFontUrl: string;
    logoUrl: string;
    name: string;
    footer: null;
    header: Header | null;
}
