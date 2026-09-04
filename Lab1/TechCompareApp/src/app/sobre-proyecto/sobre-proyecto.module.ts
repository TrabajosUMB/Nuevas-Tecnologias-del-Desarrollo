import { IonicModule } from '@ionic/angular/lazy';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SobreProyectoPage } from './sobre-proyecto.page';
import { SobreProyectoPageRoutingModule } from './sobre-proyecto-routing.module';

@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    SobreProyectoPageRoutingModule
  ],
  declarations: [SobreProyectoPage]
})
export class SobreProyectoPageModule {}
