import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SobreProyectoPage } from './sobre-proyecto.page';

const routes: Routes = [
  {
    path: '',
    component: SobreProyectoPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SobreProyectoPageRoutingModule {}
