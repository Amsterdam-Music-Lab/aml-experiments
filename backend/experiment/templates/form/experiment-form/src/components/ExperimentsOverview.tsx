import { createEntityUrl } from "../config";
import useFetch from "../hooks/useFetch";
import { Button } from "./Button";
import Page from "./Page";
import { FiPlus, FiEdit2, FiTrash2 } from "react-icons/fi";
import { Experiment, Phase, TranslatedContent } from "../types/types";
import React from "react";
import { Flag } from "./Flag";

const url = createEntityUrl('experiments');

const PhasesPills: React.FC<{ phases: Phase[] }> = ({ phases }) => {
  return (
    <div className="flex items-center">
      {phases.sort((a, b) => a.index - b.index).map((phase, idx) => (
        <React.Fragment key={phase.id}>
          {idx > 0 && <div className="h-[1px] w-4 bg-gray-300" />}
          <div className="px-2 py-1 rounded-full bg-blue-100 text-blue-800 text-xs">
            {phase.index}
          </div>
        </React.Fragment>
      ))}
    </div>
  );
};

const LanguagePills: React.FC<{ translations: TranslatedContent[] }> = ({ translations }) => {
  const languages = [...new Set(translations.map(t => t.language))];
  return (
    <div className="flex flex-wrap gap-1">
      {languages.map(lang => (
          <Flag languageCode={lang} className="h-3" />
      ))}
    </div>
  );
};

const ExperimentsOverview = () => {
  const [experiments, error, loading, fetchData] = useFetch<Experiment[]>(url);
  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this experiment?')) {
      try {
        await fetch(createEntityUrl('experiments', id.toString()), {
          method: 'DELETE',
        });
        // Refresh the page or update the list
        fetchData();
      } catch (error) {
        console.error('Error deleting experiment:', error);
      }
    }
  };

  if (error) return <div className="text-center p-4 text-red-500">Error: {error}</div>;
  const loadingClass = loading ? 'opacity-50 pointer-events-none' : '';

  async function onCreateExperiment() {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ slug: 'new-experiment', active: false }),
    });
    if (response.ok) {
      fetchData();
      // navigate to the new experiment
      const id = (await response.json()).id;
      window.location.href = `/experiments/${id}`;
    } else {
      console.error('Failed to create experiment:', response);
    }
  }


  return (
    <Page title="Experiments">
      <div className={`${loadingClass}`}>
        <div className="flex justify-end mb-4">
          <Button
            onClick={onCreateExperiment}
            variant="success"
            icon={<FiPlus />}
          >
            New Experiment
          </Button>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full bg-white shadow-md rounded">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Slug</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phases</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Languages</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {experiments?.map((experiment) => (
                <tr key={experiment.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-left whitespace-nowrap">{experiment.id}</td>
                  <td className="px-6 py-4 text-left whitespace-nowrap">{experiment.slug}</td>
                  <td className="px-6 py-4 text-left whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${experiment.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                      {experiment.active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-left whitespace-nowrap">
                    <PhasesPills phases={experiment.phases} />
                  </td>
                  <td className="px-6 py-4 text-left whitespace-nowrap">
                    <LanguagePills translations={experiment.translated_content} />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <Button
                      to={`/experiments/${experiment.id}`}
                      variant="secondary"
                      size="sm"
                      icon={<FiEdit2 />}
                      className="mr-2"
                    >
                      Edit
                    </Button>
                    <Button
                      onClick={() => experiment.id && handleDelete(experiment.id)}
                      variant="danger"
                      size="sm"
                      icon={<FiTrash2 />}
                    >
                      Delete
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Page>
  );
};

export default ExperimentsOverview;
